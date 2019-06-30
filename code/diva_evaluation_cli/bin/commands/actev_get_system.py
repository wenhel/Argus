"""Actev module: get-system

Actev modules are used to parse actev commands in order to get arguments
before calling associated entry point methods to execute systems.

Warning: this file should not be modified: see src/entry_points to add your source code.

"""
import logging

from diva_evaluation_cli.bin.commands.actev_command import ActevCommand
from diva_evaluation_cli.bin.private_src.entry_points.actev_get_system import entry_point
from diva_evaluation_cli.bin.private_src.implementation.get_system.system_types_definition import system_types

class ActevGetSystem(ActevCommand):
    """Downloads a credentialed, web-accessible content into src

    Command args:
        * url or u:           url to get the system
        * location or l:      path to store the system
        * user or U:          username to access the url
        * password or p:      password to access the url
        * token or t:         token to access the url

    """
    def __init__(self):
        super(ActevGetSystem, self).__init__('get-system', entry_point)

    def cli_parser(self, arg_parser):
        """Configure the description and the arguments (positional and optional) to parse.

        Args:
            arg_parser(:obj:`ArgParser`): Python arg parser to describe how to parse the command

        """
        arg_parser.description= "Downloads a credentialed, web-accessible content into src"
         
        sub_parser_system_types = arg_parser.add_subparsers(title='subsubcommands', dest='system_type')
        
        for system_type_name in system_types.keys():
            sub_parser_system_type = sub_parser_system_types.add_parser(system_type_name) 
            required_named = sub_parser_system_type.add_argument_group('required named arguments')

            required_named.add_argument("-u", "--url", help="url to get the system", required=True)
            
            command = system_types[system_type_name]().cli_parser(sub_parser_system_type)
            sub_parser_system_type.set_defaults(func=ActevGetSystem.command, object=self)

