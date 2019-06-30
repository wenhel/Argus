"""Entry point module: design-chunks

Implements the entry-point by using Python or any other languages.

"""
import argparse
import json

from diva_evaluation_cli.src.implementation.design_chunks import design_chunks

def entry_point(file_index, activity_index, output, nb_videos_per_chunk):
    """Method to complete: you have to raise an exception if an error occured in the program.

    Given a file index and an activity index, produce a chunks file that is suitable for the system.

    Args:
        file_index (str): Path to file index json file for test set
        activity_index (str): Path to activity index json file for test set
        output (str): Path to save chunks file
        nb_video_per_chunk (int): Number of videos in the chunk

    """
    if not nb_videos_per_chunk:
        nb_videos_per_chunk = 96
    design_chunks(file_index, activity_index, output, nb_videos_per_chunk)
