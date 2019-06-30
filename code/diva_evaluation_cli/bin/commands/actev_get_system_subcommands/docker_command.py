"""Actev module: get-system docker

Actev modules are used to parse actev commands in order to get arguments
before calling associated entry point methods to execute systems.

Warning: this file should not be modified: see src/entry_points to add your source code.

"""

from diva_evaluation_cli.bin.commands.actev_command import ActevCommand

class ActevGetSystemDocker(ActevCommand):
    """Downloads a docker image

    Command args:
        * user or U:     url to get the system
        * password or p: password to access the url

    """
    def __init__(self):
        super(ActevGetSystemDocker, self).__init__('docker', "get_docker.sh")

    def cli_parser(self, arg_parser):
        """Configure the description and the arguments (positional and optional) to parse.

        Args:
            arg_parser(:obj:`ArgParser`): Python arg parser to describe how to parse the command

        """
        arg_parser.description= "Downloads a docker image"
        required_named = arg_parser.add_argument_group('required named arguments')
        arg_parser.add_argument("-U", "--user", help="username to access the url")
        arg_parser.add_argument("-p", "--password", help="password to access the url."
                                "Warning: if password starts with \'-\', use this: --password=<your password>")

