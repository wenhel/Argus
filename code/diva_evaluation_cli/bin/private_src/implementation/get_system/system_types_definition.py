"""Get system module: system types definition

Dictionary of system types:
    * key: name of the system type
    * value: command to download the system

"""

from diva_evaluation_cli.bin.commands.actev_get_system_subcommands.docker_command import ActevGetSystemDocker
from diva_evaluation_cli.bin.commands.actev_get_system_subcommands.git_command import ActevGetSystemGit
from diva_evaluation_cli.bin.commands.actev_get_system_subcommands.other_command import ActevGetSystemOther


system_types = {
    'docker': ActevGetSystemDocker,
    'git': ActevGetSystemGit,
    'other': ActevGetSystemOther
}

