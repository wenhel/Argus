"""Main CLI module

Gather every actev command modules to parse and execute code in order to
test a system.

Warning: this file should not be modified: see src/entry_points to add your source code.
"""
import logging
import argparse
import sys

from diva_evaluation_cli.bin.commands.actev_get_system import ActevGetSystem
from diva_evaluation_cli.bin.commands.actev_system_setup import ActevSystemSetup
from diva_evaluation_cli.bin.commands.actev_validate_system import ActevValidateSystem
from diva_evaluation_cli.bin.commands.actev_design_chunks import ActevDesignChunks
from diva_evaluation_cli.bin.commands.actev_experiment_init import ActevExperimentInit
from diva_evaluation_cli.bin.commands.actev_pre_process_chunk import ActevPreProcessChunk
from diva_evaluation_cli.bin.commands.actev_process_chunk import ActevProcessChunk
from diva_evaluation_cli.bin.commands.actev_post_process_chunk import ActevPostProcessChunk
from diva_evaluation_cli.bin.commands.actev_reset_chunk import ActevResetChunk
from diva_evaluation_cli.bin.commands.actev_experiment_cleanup import ActevExperimentCleanup
from diva_evaluation_cli.bin.commands.actev_merge_chunks import ActevMergeChunks
from diva_evaluation_cli.bin.commands.actev_exec import ActevExec
from diva_evaluation_cli.bin.commands.actev_status import ActevStatus
from diva_evaluation_cli.bin.commands.actev_validate_execution import ActevValidateExecution

private_subcommands = [
ActevGetSystem(),
ActevValidateSystem(),
ActevExec(),
ActevStatus(),
ActevValidateExecution()
]

public_subcommands = [
ActevSystemSetup(),
ActevDesignChunks(),
ActevExperimentInit(),
ActevPreProcessChunk(),
ActevProcessChunk(),
ActevPostProcessChunk(),
ActevResetChunk(),
ActevMergeChunks(),
ActevExperimentCleanup(),
]

def cli_parser():
    """ Main command to parse commands and arguments
    """
    # Initialize logger
    logging.getLogger().setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('[%(asctime)s] diva_evaluation_cli-%(levelname)s: %(message)s'))
    logging.getLogger().addHandler(handler)

    # Initialize parser
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(title='subcommands')
    subparsers = {}

    subcommands = private_subcommands + public_subcommands
    # Initialize subparsers
    for subcommand in subcommands:
        subparser = subs.add_parser(subcommand.command)
        subparsers[subcommand.command] = subparser
        subcommand.cli_parser(subparsers[subcommand.command])

    args = parser.parse_args()
    if hasattr(args, 'func') and args.func:
        args.func(args.object, args)
    else:
        parser.print_help()

def main():
    cli_parser()

if __name__ == '__main__':
    main()
