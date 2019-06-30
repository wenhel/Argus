"""Entry point module: exec

This file should not be modified.
"""
import os

def entry_point(file_index, activity_index, chunks, nb_videos_per_chunk,
    video_location, system_cache_dir, output_file, chunks_result, config_file=None):
    """Private entry point.

    Calls a team-implemented API. Captures time stamps, resource usage, etc.

    Args:
        file_index (str): Path to file index json file for test set
        activity_index (str): Path to activity index json file for test set
        chunks (str): Path to chunks json file
        nb-video-per-chunk (int): Number of videos in the chunk
        video-location (str): Path to videos content
        system-cache-dir (str): Path to system cache directory
        output-file (str): Path to merge chunks command result
        chunk_result (str): Path to chunks json file after merge chunks execution
        config_file (str, optional): Path to config file

    """
    if not nb_videos_per_chunk:
        nb_videos_per_chunk = "300"

    if not config_file:
        config_file = "None"

    # go into the right directory to execute the script
    path = os.path.dirname(__file__)
    script = os.path.join(path, '../implementation/exec/exec.sh')
    script += " " + file_index + \
              " " + activity_index + \
              " " + chunks + \
              " " + nb_videos_per_chunk + \
              " " + video_location + \
              " " + system_cache_dir + \
              " " + config_file + \
              " " + output_file + \
              " " + chunks_result

    # execute the script
    # status is the exit status code returned by the program
    status = os.system(script)
    if status != 0:
        raise Exception("Error occured in exec.sh")
