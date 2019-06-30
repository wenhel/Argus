"""Actev module: validate-execution

Actev modules are used to parse actev commands in order to get arguments
before calling associated entry point methods to execute systems.

Warning: this file should not be modified: see src/entry_points to add your source code.

"""
import logging

from diva_evaluation_cli.bin.commands.actev_command import ActevCommand
from diva_evaluation_cli.bin.private_src.entry_points.actev_validate_execution import entry_point


class ActevValidateExecution(ActevCommand):
    """Test the execution of the system on each validation data set provided in container_output directory.

    Compare the newly generated to the expected output and the reference.

    Command args:
        * output of o:         path to experiment output json file
        * reference or r:      path to reference json file
        * file-index or f:     path to file index json file for test set
        * activity-index or a: path to activity index json file for test set
        * result or -R:        path to result of the ActEV scorer

    """
    def __init__(self):
        super(ActevValidateExecution, self).__init__('validate-execution', entry_point)

    def cli_parser(self, arg_parser):
        """Configure the description and the arguments (positional and optional) to parse.

        Args:
            arg_parser(:obj:`ArgParser`): Python arg parser to describe how to parse the command

        """
        arg_parser.description = "Test the execution of the system on each validation data set provided"
        required_named = arg_parser.add_argument_group('required named arguments')

        required_named.add_argument("-o", "--output", help="path to experiment output json file", required=True)
        required_named.add_argument("-r", "--reference", help="path to reference json file", required=True)
        required_named.add_argument("-a", "--activity-index", help="path to activity index json file", required=True)
        required_named.add_argument("-f", "--file-index", help="path to file index json file", required=True)
        required_named.add_argument("-R", "--result", help="path to result of the ActEV scorer", required=True)

        arg_parser.set_defaults(func=ActevValidateExecution.command, object=self)
