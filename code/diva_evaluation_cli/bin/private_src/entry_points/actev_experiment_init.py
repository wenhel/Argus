"""Entry point module: experiment-init

This file should not be modified.
"""
import os

from diva_evaluation_cli.bin.private_src.implementation.experiment_init.experiment_validation import experiment_validation

def before_entry_point(file_index, activity_index, chunks, 
    video_location, system_cache_dir, config_file=None):
    """Private entry point.

    Start servers, starts cluster, etc.

    Args:
        file_index(str): Path to file index json file for test set
        activity_index(str): Path to activity index json file for test set
        chunks (str): Path to chunks json file
        video_location (str): Path to videos content
        system_cache_dir (str): Path to system cache directory
        config_file (str, optional): Path to config file

    """
    experiment_validation(file_index, video_location)

