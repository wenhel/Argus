"""Actev module: validate-system

Actev modules are used to parse actev commands in order to get arguments
before calling associated entry point methods to execute systems.

Warning: this file should not be modified: see src/entry_points to add your source code.

"""

import logging

from diva_evaluation_cli.bin.commands.actev_command import ActevCommand
from diva_evaluation_cli.bin.private_src.entry_points.actev_validate_system import entry_point


class ActevValidateSystem(ActevCommand):
    """Checks the structure of the  directory after ActEV-system-setup is run. Checks for expected API contents, etc.
    """
    def __init__(self):
        super(ActevValidateSystem, self).__init__('validate-system', entry_point)

    def cli_parser(self, arg_parser):
        """ Configure the description and the arguments (positional and optional) to parse.

        Args:
            arg_parser(:obj:`ArgParser`): Python arg parser to describe how to parse the command

        """
        arg_parser.description = "Checks the structure of the  directory after ActEV-system-setup is run"
        arg_parser.set_defaults(func=ActevValidateSystem.command, object=self)
