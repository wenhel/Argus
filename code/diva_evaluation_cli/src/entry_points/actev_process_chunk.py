"""Entry point module: process-chunk

Implements the entry-point by using Python or any other languages.

"""
import os
import re

def entry_point(chunk_id, system_cache_dir):
    """Method to complete: you have to raise an exception if an error occured in the program.

    Process a chunk.

    Args:
        chunk_id (str): Chunk id
        system_cache_dir (str): Path to system cache directory

    """
    # get the int inside the id
    chunk_key = re.search('Chunk([0-9]+)', chunk_id).group(1)

    # go into the right directory to execute the script
    path = os.path.dirname(__file__)
    script = os.path.join(path, '../implementation/process_chunk.sh')

    # execute the script
    # status is the exit status code returned by the program
    status = os.system("%s %s" % (script, chunk_key))
    if status != 0:
        raise Exception("Error occured in process_chunk.sh")
