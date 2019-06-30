"""Validate system module

Used by the command validate-system
"""
import inspect
import importlib
import logging
import os
import sys

root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../../')

def validate_system():
    """Main validation method
    """
    validate_structure()
    validate_cli()
    validate_container_output()
    logging.info("System is valid")

############################### structure #####################################

def validate_structure():
    """Validate structure of the CLI: should contain required directories.
    """
    directories = os.listdir(root_path)
    content = import_expected_result('expected_structure.txt')
    logging.info("Structure validation")

    for directory in content:
        if not directory in directories:
            raise Exception("System validation failed, missing {} directory".format(directory))
        if not os.path.isdir(root_path + '/'  + directory):
            raise Exception("System validation failed, {} not a directory".format(directory))
        logging.info("    .. {} is valid".format(directory))

################################## cli ########################################

def validate_cli():
    """ Import the entry points method and try to compare them with the expected result
    """
    from diva_evaluation_cli.bin.cli import public_subcommands

    # Open expected result
    content = import_expected_result('expected_validation_result.txt')
    i = 0
    logging.info("CLI validation")

    for subcommand in public_subcommands:
        actev_command = "actev_" + subcommand.command.replace('-', '_')

        # Is entry point exist
        try:
            entry_point_module = importlib.import_module('diva_evaluation_cli.src.entry_points.{}'.format(actev_command))
        except:
            raise Exception("System validation failed, {} entry_point method removed".format(actev_command))

        entry_point_function = getattr(entry_point_module, 'entry_point')
        result = "{} - {}".format(actev_command,inspect.signature(entry_point_function))

        # Is entry point contain correct arguments
        if content[i] != result:
            raise Exception("System validation failed, {} entry_point method changed".format(actev_command))
        i += 1
        logging.info("    .. {} is valid".format(actev_command))

def import_expected_result(file_name):
    """ Import expected validation result

    Args:
        file_name (str): Path to file to open in order to extract lines inside a list

    """
    content = []
    path = os.path.dirname(__file__)
    expected_result = os.path.join(path, file_name)
    with open(expected_result, 'r') as f:
        content = f.readlines()
    content = [line.strip() for line in content]
    return content

############################# container output ################################

def validate_container_output():
    """ Check that container output directory is present.
    For each datasetID directory, chunks, activity, file and output should be present too.
    """
    container_output_dir = os.path.join(root_path, 'container_output')
    logging.info("Container output validation")

    for dataset_id in os.listdir(container_output_dir):
        dataset_id_path = os.path.join(container_output_dir, dataset_id)
        if os.path.isdir(dataset_id_path):
            files = os.listdir(dataset_id_path)
            content = import_expected_result('expected_container_output.txt')
            for file_name in content:
                dataset_filename = dataset_id + '_' + file_name
                if not dataset_filename in files:
                    raise Exception("System validation failed, {} not present in {}".format(dataset_filename, dataset_id))
            logging.info("    .. {} is valid".format(dataset_id))

