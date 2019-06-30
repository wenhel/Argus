"""Entry point module: post-process-chunk

Implements the entry-point by using Python or any other languages.

"""
import os

def entry_point(chunk_id, system_cache_dir):
    """Method to complete: you have to raise an exception if an error occured in the program.

    Post-process a chunk.

    Args:
        chunk_id (str): Chunk id
        system_cache_dir (str): Path to system cache directory

    """
    # go into the right directory to execute the script
    path = os.path.dirname(__file__)
    script = os.path.join(path, '../implementation/post_process_chunk.sh')

    # execute the script
    # status is the exit status code returned by the program
    status = os.system("%s %s" % (script, chunk_id))
    if status != 0:
    	raise Exception("Error occured in post_process_chunk.sh")
