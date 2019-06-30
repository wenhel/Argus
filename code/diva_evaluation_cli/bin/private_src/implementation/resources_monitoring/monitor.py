# -*- coding: utf-8 -*-
"""Monitor module

This module implements the Module class, which monitors the execution
of a running process

Attributes:
    logger (:obj:`logging.logger`): Logger of the current module

"""

import json
import os
import psutil
import datetime, time
import logging

from multiprocessing import *

from diva_evaluation_cli.bin.private_src.implementation.resources_monitoring.nvml_handler import NvmlHandler
from diva_evaluation_cli.bin.private_src.implementation.resources_monitoring import utils


logger = logging.getLogger('MONITOR')


class Monitor():
    """Class that implements a monitor

    A Monitor object contains a python function
    that will be run in parallel with a monitor process.
    Once the `main_function` terminates, the monitoring thread terminates.

    Attributes:
        main_function (function): Python function that will be run as a subprocess and monitored
        args (Namespace): Arguments given when executing the `main_function`
        command_name (str): Name of the command that will be monitored
        interval (int): Interval (in *s*) to poll the system resources
        log_file (str): File path to the logs file

    """

    def __init__(self, main_function, args, command_name='default_command', interval=5):
        """
        Args:
            main_function (function): Python function that will be run as a subprocess and monitored
            args (Namespace): Arguments given when executing the `main_function`
            command_name (str, optional): Name of the command that will be monitored
            interval (int, optional): Interval (in *s*) to poll the system resources

        """
        self.command_name = command_name
        self.main_function = main_function
        self.args = args
        self.interval = interval

        log_file_path = os.path.dirname(__file__)
        self.log_file = os.path.join(log_file_path, './resources_monitoring.json')



    def run_monitor(self):
        """Runs the monitoring process

        The `main_function` in a process and the
        `monitoring_process()` function in another.

        """

        self.main_process = Process(target=self.main_function, kwargs=self.args.__dict__)
        self.main_process.start()

        self.monitor = Process(target=self.monitor_resources)
        self.monitor.start()

        while self.main_process.exitcode is None:
            pass

        if self.main_process.exitcode != 0:
            raise Exception
            

    def increment_log_file(self, log_dict):
        """Increment the file pointed by the `log_file` attribute with a new dict

        Note:
            The existing `log_file` will be overwritten it it fails to load using JSON.load()

        Args:
            log_dict (:obj:`dict`) A new dictionary to increment the existing log_file

        """

        with open(self.log_file, 'a') as f:
                f.write(json.dumps(log_dict) + ',\n')

    def monitor_resources(self):
        """Fuction that runs every `interval` seconds to get the status of the
        `main_process`

        Note:
            The tried/catched block prevents the case where
            the process supposed to be monitored is already gone

        """

        # Try to retrieve the main_process
        try:
            process = psutil.Process(self.main_process.pid)

            # Load the NVIDIA handler
            with NvmlHandler() as nvml_h:
                while process.is_running() and process.status() != psutil.STATUS_ZOMBIE:

                    # Gather resources use from psutil
                    resources_use = utils.psutil_snapshot()

                    # Get status from the GPUs
                    resources_use.update({'gpus':nvml_h.get_devices_status()})

                    # Get the command that's currently run
                    resources_use.update({'command_line':self.command_name})

                    # Update the timestamp
                    resources_use.update({'timestamp':datetime.datetime.now().isoformat()})

                    # Increment the logs file
                    self.increment_log_file(resources_use)

                    time.sleep(self.interval)

        except Exception as e:
            logger.debug(e)
            logger.debug('PID {} not available for monitoring'.format(self.main_process.pid))
