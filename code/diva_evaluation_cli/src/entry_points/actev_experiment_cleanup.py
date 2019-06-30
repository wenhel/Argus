"""Entry point module: experiment-cleanup

Implements the entry-point by using Python or any other languages.

"""
import os

def entry_point():
    """Method to complete: you have to raise an exception if an error occured in the program.

    Close any servers, terminates cluster (future functionality), etc.

    """
    # go into the right directory to execute the script
    path = os.path.dirname(__file__)
    script = os.path.join(path, '../implementation/clean_up.sh')

    # execute the script
    # status is the exit status code returned by the program
    status = os.system(script)
    if status != 0:
    	raise Exception("Error occured in clean_up.sh")
