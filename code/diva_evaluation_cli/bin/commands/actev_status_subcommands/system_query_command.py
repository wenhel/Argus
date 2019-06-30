"""Actev module: system-query

Actev modules are used to parse actev commands in order to get arguments
before calling associated entry point methods to execute systems.

Warning: this file should not be modified: see src/entry_points to add your source code.

"""


from diva_evaluation_cli.bin.commands.actev_command import ActevCommand

class ActevStatusSystemQuery(ActevCommand):
    """Get the status of the system
    """
    def __init__(self):
        super(ActevStatusSystemQuery, self).__init__('system-query', '')

    def cli_parser(self, arg_parser):
        """Configure the description and the arguments (positional and optional) to parse.

        Args:
            arg_parser(:obj:`ArgParser`): Python arg parser to describe how to parse the command

        """
        arg_parser.description= "Get the status of the system"
        required_named = arg_parser.add_argument_group('required named arguments')

