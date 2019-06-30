"""Actev module: status

Actev modules are used to parse actev commands in order to get arguments
before calling associated entry point methods to execute systems.

Warning: this file should not be modified: see src/entry_points to add your source code.

"""

import logging

from diva_evaluation_cli.bin.commands.actev_command import ActevCommand
from diva_evaluation_cli.bin.private_src.entry_points.actev_status import entry_point
from diva_evaluation_cli.bin.private_src.implementation.status.query_types_definition import query_types

class ActevStatus(ActevCommand):
    """Executable at any time. Get the status of the experiment.
    """
    def __init__(self):
        super(ActevStatus, self).__init__('status', entry_point)

    def cli_parser(self, arg_parser):
        """Configure the description and the arguments (positional and optional) to parse.

        Args:
            arg_parser(:obj:`ArgParser`): Python arg parser to describe how to parse the command

        """
        arg_parser.description= "Executable at any time. Get the status of the experiment"

        sub_parser_query_types = arg_parser.add_subparsers(title='subsubcommands', dest='query_type')

        for query_type_name in query_types.keys():
            sub_parser_query_type = sub_parser_query_types.add_parser(query_type_name)
            required_named = sub_parser_query_type.add_argument_group('required named arguments')

            command = query_types[query_type_name]().cli_parser(sub_parser_query_type)
            sub_parser_query_type.set_defaults(func=ActevStatus.command, object=self)


