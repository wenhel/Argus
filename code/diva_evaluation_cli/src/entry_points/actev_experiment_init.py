"""Entry point module: experiment-init

Implements the entry-point by using Python or any other languages.

"""
import os

def entry_point(file_index, activity_index, chunks,
    video_location, system_cache_dir, config_file=None):
    """Method to complete: you have to raise an exception if an error occured in the program.

    Start servers, starts cluster, etc.

    Args:
        file_index(str): Path to file index json file for test set
        activity_index(str): Path to activity index json file for test set
        chunks (str): Path to chunks json file
        video_location (str): Path to videos content
        system_cache_dir (str): Path to system cache directory
        config_file (str, optional): Path to config file

    """
    # go into the right directory to execute the script
    path = os.path.dirname(__file__)
    script = os.path.join(path, '../implementation/init_experiment.sh')
    script += " " + file_index + \
              " " + activity_index + \
              " " + chunks + \
              " " + video_location + \
              " " + system_cache_dir

    # execute the script
    # status is the exit status code returned by the program
    status = os.system(script)
    if status != 0:
        raise Exception("Error occured in init_experiment.sh")
