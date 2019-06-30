"""Experiment init module

"""
import os
import json

def experiment_validation(file_index, video_location):
    """ Check that every video files enumerated in file_index exists, is readable and has content.

    Args:
        file_index (str): Path to file index in json
        video_location (str): Path to directory containing videos

    """
    with open(file_index) as f:
        file_dict = json.load(f)

    if not os.path.isdir(video_location):
        raise Exception("Invalid argument: video_location is not a directory")

    for video_filename in file_dict:
        file_index_exists = False

        for dirpath, dirnames, filenames in os.walk(video_location):
            for filename in filenames:
                if filename == video_filename:
                    file_index_exists = True
                    video = os.path.join(dirpath, filename)
                    if not os.path.isfile(video):
                        raise Exception("Invalid file index: {} is not a file".format(video))
                    if os.stat(video).st_size == 0:
                        raise Exception("Invalid file index: {} is empty.".format(video))

        if not file_index_exists:
            raise Exception("Invalid file index: {} does not exist".format(video_filename))
