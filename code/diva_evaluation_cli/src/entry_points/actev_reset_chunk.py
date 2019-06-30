"""Entry point module: reset-chunk

Implements the entry-point by using Python or any other languages.

"""
import os

def entry_point(chunk_id, system_cache_dir):
    """Method to complete: you have to raise an exception if an error occured in the program.

    Delete all cached information for ChunkID so that the chunk can be re-run.

    Args:
        chunk_id (str): Chunk id
        system_cache_dir (str): Path to system cache directory
    """
    if not system_cache_dir:
        raise Exception("reset_chunk.sh needs system-cache-dir argument, please provide it")

    # go into the right directory to execute the script
    path = os.path.dirname(__file__)
    script = os.path.join(path, '../implementation/reset_chunk.sh')

    # execute the script
    # status is the exit status code returned by the program
    status = os.system("%s %s %s" % (script, chunk_id, system_cache_dir))
    if status != 0:
        raise Exception("Error occured in reset_chunk.sh")
