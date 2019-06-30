"""Entry point module: validate-execution

This file should not be modified.
"""
import os

def entry_point(output, reference, activity_index, file_index, result):
    """Private entry point.

    Test the execution of the system on each validation data set provided in container_output directory

    Args:
        output (str): Path to experiment output json file
        reference (str): Path to reference json file
        file_index (str): Path to file index json file for test set
        activity_index (str): Path to activity index json file for test set
        result (str): Path to result of the ActEV scorer

    """
    # go into the right directory to execute the script
    path = os.path.dirname(__file__)
    execution_validation_dir = os.path.join(path, '../implementation/validate_execution')

    installation_script = os.path.join(execution_validation_dir, 'install.sh')
    script = os.path.join(execution_validation_dir, 'score.sh')
    script += " " + output + \
              " " + reference + \
              " " + activity_index + \
              " " + file_index + \
              " " + result

    # execute the script
    # status is the exit status code returned by the program
    status = os.system('cd ' + execution_validation_dir + \
                       ';. ' + installation_script + \
                       ';' + script)
    if status != 0:
        raise Exception("Error occured in install.sh or score.sh")

