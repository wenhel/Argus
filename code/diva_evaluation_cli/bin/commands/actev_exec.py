"""Actev module: exec

Actev modules are used to parse actev commands in order to get arguments
before calling associated entry point methods to execute systems.

Warning: this file should not be modified: see src/entry_points to add your source code.

"""
import logging

from diva_evaluation_cli.bin.commands.actev_command import ActevCommand
from diva_evaluation_cli.bin.private_src.entry_points.actev_exec import entry_point

class ActevExec(ActevCommand):
    """Calls a team-implemented API. Captures time stamps, resource usage, etc.

    Command args:
        * file-index or f:         path to file index json file for test set
        * activity-index or a:     path to activity index json file for test set
        * chunks or c:             path to chunks json file
        * nb-video-per-chunk or n: number of videos in the chunk
        * video-location or v:     path to videos content
        * system-cache-dir or s:   path to system cache directory
        * config-file or C:        path to config file
        * output-file:             path to merge chunks command result
        * chunk_result:            path to chunks json file after merge chunks execution

    """
    def __init__(self):
        super(ActevExec, self).__init__('exec', entry_point)

    def cli_parser(self, arg_parser):
        """Configure the description and the arguments (positional and optional) to parse.

        Args:
            arg_parser(:obj:`ArgParser`): Python arg parser to describe how to parse the command

        """
        arg_parser.description= "Calls a team-implemented API. Captures time stamps, resource usage, etc."
        required_named = arg_parser.add_argument_group('required named arguments')

        required_named.add_argument("-f", "--file-index", help="path to file index json file", required=True)
        required_named.add_argument("-a", "--activity-index", help="path to activity index json file", required=True)
        required_named.add_argument("-c", "--chunks", help="path to chunks json file", required=True)
        arg_parser.add_argument("-n", "--nb-videos-per-chunk", help="number of videos in a chunk")

        required_named.add_argument("-v", "--video-location", help="path to videos content", required=True)
        required_named.add_argument("-s", "--system-cache-dir", help="path to system cache directory", required=True)
        arg_parser.add_argument("-C", "--config-file", help="path to config file")

        required_named.add_argument("-o", "--output-file", help="path to merge chunks command result", required=True)
        required_named.add_argument("-r", "--chunks-result", help="path to chunks json file after merge chunks execution", required=True)
        arg_parser.set_defaults(func=ActevExec.command, object=self)

