"""Actev module: merge-chunks

Actev modules are used to parse actev commands in order to get arguments
before calling associated entry point methods to execute systems.

Warning: this file should not be modified: see src/entry_points to add your source code.

"""
from diva_evaluation_cli.bin.commands.actev_command import ActevCommand
from diva_evaluation_cli.src.entry_points.actev_merge_chunks import entry_point


class ActevMergeChunks(ActevCommand):
    """Given a list of chunk ids, merges all the chunks system output present in the list.

    Command args:
        * result-location or r: path to get the result of the chunks processing
        * chunk-file or c:      path to directory where intermediate system output is stored
        * output-file or o:     path to the output file generated
        * chunk-ids or i:       list of chunk ids

    """
    def __init__(self):
        super(ActevMergeChunks, self).__init__('merge-chunks', entry_point)

    def cli_parser(self, arg_parser):
        """Configure the description and the arguments (positional and optional) to parse.

        Args:
            arg_parser(:obj:`ArgParser`): Python arg parser to describe how to parse the command

        """
        arg_parser.description = "Merge given chunk ids in a file and output NIST compliant system file"
        required_named = arg_parser.add_argument_group('required named arguments')

        required_named.add_argument("-r", "--result-location", help="path to get the result of the chunks processing", required=True)
        required_named.add_argument("-o", "--output-file", help="path to save the output file generated", required=True)
        required_named.add_argument("-c", "--chunks-file", help="path to save the chunks in a json file", required=True)
        arg_parser.add_argument("-i", "--chunk-ids", help="list of chunk ids", nargs='+')
        arg_parser.set_defaults(func=ActevMergeChunks.command, object=self)
