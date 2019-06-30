"""Actev module

Actev modules are used to parse actev commands in order to get arguments
before calling associated entry point methods to execute systems.

Warning: this file should not be modified: see src/entry_points to add your source code.
"""
import abc
import logging
import sys

from diva_evaluation_cli.bin.private_src.implementation.resources_monitoring.monitor import Monitor
from diva_evaluation_cli.bin.private_src.implementation.status.status_factory import StatusFactory

class ActevCommand():
    """ Abstract class that represents an actev command.

    Every actev modules must inherit from this class and
    implement the following methods

    Attributes:
        command (str): Name of the actev command
        entry_point (function): Python function that represents an entry point
        before_entry_point (function, optional): Python function that should be executed before entry_point method
        after_entry_point (function, optional): Python function that should be executed after entry_point method

    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, command, entry_point, before_entry_point=None, after_entry_point=None):
        """
        Args:
            command (str): Name of the actev command
            entry_point (function): Python function that represents an entry point
            before_entry_point (function, optional): Python function that should be executed before entry_point method
            after_entry_point (function, optional): Python function that should be executed after entry_point method

        """
        self.command = command
        self.entry_point = entry_point
        self.before_entry_point = before_entry_point
        self.after_entry_point = after_entry_point

    @abc.abstractmethod
    def cli_parser(self, arg_parser):
        """ Configure the description and the arguments (positional and optional) to parse.

        Args:
            arg_parser(:obj:`ArgParser`): Python arg parser to describe how to parse the command

        """
        return

    def before_command(self, args):
        """ Execute an action before executing the command

        Args:
            args (:obj:`dict`): contains the arguments passed during the actev command call

        """
        if self.before_entry_point:
            self.before_entry_point(**args.__dict__)

    def after_command(self, args):
        """ Execute an action after executing the command

        Args:
            args (:obj:`dict`): contains the arguments passed during the actev command call

        """
        if self.after_entry_point:
            self.after_entry_point(**args.__dict__)

    def command(self, args):
        """ Gets arguments and passe them to an entry point. Catch the exception occured.

        Args:
            args (:obj:`dict`): contains the arguments passed during the actev command call

        """
        del args.__dict__['object']
        del args.__dict__['func']

        try:
            logging.info("Starting %s" % self.command)
            StatusFactory.generate_status(self, 'start', args.__dict__)

            self.before_command(args)
            mon = Monitor(self.entry_point, args, self.command)
            mon.run_monitor() 
            self.after_command(args)

            logging.info("%s done" % self.command)
            StatusFactory.generate_status(self, 'done', args.__dict__)
        except:
            logging.error("Issue during %s" % self.command)
            StatusFactory.generate_status(self, 'issue', args.__dict__)
            sys.exit(1)

