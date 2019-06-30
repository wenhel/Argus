# -*- coding: utf-8 -*-
"""NVML Handler module

This module implements the NvmlHandler class, which interacts with the NVML
module to monitor the status of the NVIDIA GPU hardware

Attributes:
    logger (:obj: `logging.logger`): Logger of the current module

"""

from pynvml import *
import logging

from diva_evaluation_cli.bin.private_src.implementation.resources_monitoring import utils


logger = logging.getLogger('MONITOR')

class NvmlHandler():
    """Class to wrap the function to monitor NVIDIA GPUs using the pynvml package.

    This class is instanciated using a context manager to ensure that the NVML
    pointers are destroyed.

    Attributes:
        devices (:obj:`dict` of :obj:`NvmlObjects`): references pointers to the NVIDIA devices

    Example:
        with NvmlHandler() as nvml_handler:
            nvml_handler.get_devices_status()

    """

    def __init__(self):
        """Init the connection with NVML,
        And stores the device handlers in a dictionary

        """
        nvmlInit()
        n_devices = nvmlDeviceGetCount()
        devices_handlers_list = [nvmlDeviceGetHandleByIndex(i) for i in range(n_devices)]

        self.devices = {
            '{}-{}'.format(NvmlHandler.exec_nvml_function(nvmlDeviceGetName, device).decode('ascii'), i): device
            for i, device in  enumerate(devices_handlers_list)
        }

    def __enter__(self):
        """Called when instanciating the Object using a with: block

        """
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        """Called to destroy the pointer to NVML

        """
        nvmlShutdown()


    def get_devices_status(self):
        """Get the status of the devices referenced in `devices`

        Returns:
            {"device_name": {"key":"value", ...}, ...} with some relevant information from NVML

        """
        return {

                dev_name:{
                    'running_processes': self.get_running_processes(dev_handler),
                    'gpu_memory_free': utils.psutil_parse_readable_bytes(
                                        NvmlHandler.exec_nvml_function(nvmlDeviceGetMemoryInfo, dev_handler, 'free')
                                ),
                    'gpu_memory_used': utils.psutil_parse_readable_bytes(
                                        NvmlHandler.exec_nvml_function(nvmlDeviceGetMemoryInfo, dev_handler, 'used')
                                )
            } for dev_name, dev_handler in self.devices.items()
        }

    def get_running_processes(self, dev_handler):
        """Use the NVML's nvmlDeviceGetComputeRunningProcesses to get processes using the GPU,
        And get some information about these processes using the psutil module

        """
        # Get the list of running processes on each device
        running_processes = NvmlHandler.exec_nvml_function(nvmlDeviceGetComputeRunningProcesses,dev_handler)

        # Turns these process objects into dicts
        running_processes_dicts = [obj.__dict__ for obj in running_processes  if obj]

        # Enhance these dicts with information from psutil
        new_dicts = []
        for running_processes_dict in running_processes_dicts:

            # Init the new dict with the current information
            more_ps_infos = {}
            more_ps_infos.update(running_processes_dict)

            # Rename the usedGpuMemory key, if any
            if 'usedGpuMemory' in more_ps_infos:
                more_ps_infos['gpu_memory_used'] = utils.psutil_parse_readable_bytes(
                    more_ps_infos.get('usedGpuMemory')
                )
                del more_ps_infos['usedGpuMemory']

            # Try to retreive info about the process using psutil
            try:
                pid = running_processes_dict.get('pid')
                more_ps_infos.update(utils.psutil_snapshot_process(pid))
            except Exception as e:
                logger.warning('Cannot gather info from process {}'.format(pid))

            new_dicts.append(more_ps_infos)

        return new_dicts

    @staticmethod
    def exec_nvml_function(nvml_func, dev_handler, attr=None):
        """Wrapper arount the NVML functions: they will send exceptions
        if an attribute is unavailable

        Args:
            nvml_func (:`function`): NVML function to execute
            dev_handler (:obj:`NvmlObjects`): Pointer to a device
            attr (str, optional): Attribute to get from the object returned from `nvml_func`

        """
        try:
            obj = nvml_func(dev_handler)
            if attr:
                return getattr(obj, attr)
            return obj

        except Exception as e:
            return None
