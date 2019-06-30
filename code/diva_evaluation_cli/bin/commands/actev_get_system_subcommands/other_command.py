"""Actev module: get-system other

Actev modules are used to parse actev commands in order to get arguments
before calling associated entry point methods to execute systems.

Warning: this file should not be modified: see src/entry_points to add your source code.

"""
from diva_evaluation_cli.bin.commands.actev_command import ActevCommand

class ActevGetSystemOther(ActevCommand):
    """Downloads a web resources as a tar file

    Command args:
        * location or l: path to store the system
        * user or U:     url to get the system
        * password or p: password to access the url
        * token or t:    token to access the url

    """
    def __init__(self):
        super(ActevGetSystemOther, self).__init__('other', "get_other.sh")

    def cli_parser(self, arg_parser):
        """Configure the description and the arguments (positional and optional) to parse.

        Args:
            arg_parser(:obj:`ArgParser`): Python arg parser to describe how to parse the command

        """
        arg_parser.description= "Downloads a web resources as a tar file"
        required_named = arg_parser.add_argument_group('required named arguments')
        arg_parser.add_argument("-U", "--user", help="username to access the url"
                                "Warning: if password starts with \'-\', use this: --password=<your password>")
        arg_parser.add_argument("-p", "--password", help="password to access the url")
        arg_parser.add_argument("-l", "--location", help="path to store the system")
        arg_parser.add_argument("-t", "--token", help="token to access the url"
                                "Warning: if token starts with \'-\', use this: --token=<your token>")


