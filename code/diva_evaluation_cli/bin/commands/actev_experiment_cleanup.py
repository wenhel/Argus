"""Actev module: experiment-cleanup

Actev modules are used to parse actev commands in order to get arguments
before calling associated entry point methods to execute systems.

Warning: this file should not be modified: see src/entry_points to add your source code.

"""
import logging

from diva_evaluation_cli.bin.commands.actev_command import ActevCommand
from diva_evaluation_cli.src.entry_points.actev_experiment_cleanup import entry_point


class ActevExperimentCleanup(ActevCommand):
    """Close any servers, terminates cluster (future functionality), etc.
    """

    def __init__(self):
        super(ActevExperimentCleanup, self).__init__('experiment-cleanup', entry_point)

    def cli_parser(self, arg_parser):
        """Configure the description and the arguments (positional and optional) to parse.

        Args:
            arg_parser(:obj:`ArgParser`): Python arg parser to describe how to parse the command

        """
        arg_parser.description = "Close any servers, terminates cluster, etc."
        arg_parser.set_defaults(func=ActevExperimentCleanup.command, object=self)
