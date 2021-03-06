"""Actev module: reset-chunk

Actev modules are used to parse actev commands in order to get arguments
before calling associated entry point methods to execute systems.

Warning: this file should not be modified: see src/entry_points to add your source code.

"""
import logging

from diva_evaluation_cli.bin.commands.actev_command import ActevCommand
from diva_evaluation_cli.src.entry_points.actev_reset_chunk import entry_point


class ActevResetChunk(ActevCommand):
    """Delete all cached information for ChunkID so that the chunk can be re-run.

    Command args:
        * chunk-id or i: chunk id
        * system-cache-dir or s: path to system cache directory

    """
    def __init__(self):
        super(ActevResetChunk, self).__init__('reset-chunk', entry_point)

    def cli_parser(self, arg_parser):
        """Configure the description and the arguments (positional and optional) to parse.

        Args:
            arg_parser(:obj:`ArgParser`): Python arg parser to describe how to parse the command

        """
        arg_parser.description = "Delete all cached information"
        required_named = arg_parser.add_argument_group('required named arguments')

        required_named.add_argument("-i", "--chunk-id", help="chunk id", required=True)
        arg_parser.add_argument("-s", "--system-cache-dir", help="path to system cache directory")
        arg_parser.set_defaults(func=ActevResetChunk.command, object=self)
