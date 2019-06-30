"""Actev module: design-chunks

Actev modules are used to parse actev commands in order to get arguments
before calling associated entry point methods to execute systems.

Warning: this file should not be modified: see src/entry_points to add your source code.

"""
from diva_evaluation_cli.bin.commands.actev_command import ActevCommand
from diva_evaluation_cli.src.entry_points.actev_design_chunks import entry_point


class ActevDesignChunks(ActevCommand):
    """Given a file index and an activity index, produce a chunks file that is suitable for the system.

    Command args:
        * file-index or f:         path to file index json file for test set
        * activity-index or a:     path to activity index json file for test set
        * output or o:             path to save chunks file
        * nb_video-per-chunk or n: number of videos in the chunk

    """
    def __init__(self):
        super(ActevDesignChunks, self).__init__('design-chunks', entry_point)

    def cli_parser(self, arg_parser):
        """Configure the description and the arguments (positional and optional) to parse.

        Args:
            arg_parser(:obj:`ArgParser`): Python arg parser to describe how to parse the command

        """
        arg_parser.description = "Produce a chunks file that is suitable for the system"
        required_named = arg_parser.add_argument_group('required named arguments')

        required_named.add_argument("-f", "--file-index", help="path to file index json file", required=True)
        required_named.add_argument("-a", "--activity-index", help="path to activity index json file", required=True)
        required_named.add_argument("-o", "--output", help="path to save chunks file", required=True)
        arg_parser.add_argument("-n", "--nb-videos-per-chunk", type=int, help="number of videos in a chunk")
        arg_parser.set_defaults(func=ActevDesignChunks.command, object=self)
