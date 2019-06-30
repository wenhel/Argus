"""Entry point module: get-system

This file should not be modified.
"""
import os
from diva_evaluation_cli.bin.private_src.implementation.get_system.system_types_definition import system_types

def entry_point(url, system_type, location=None, user=None, password=None, token=None, install_cli=False):
    """Private entry point.

    Downloads a credentialed, web-accessible content into src

    Args:
        url (str): Url to get the system
        location (str, optional): Path to store the system
        user (str, optional): Username to access the url
        password (str, optional): Password to access the url
        token (str, optional): Token to access the url
        install_cli (bool, optional): Information to know wether CLI has to be installed

    """
    try:
        command = system_types[system_type]()
        script = command.entry_point
    except:
        raise Exception("Unknown system type")

    if not location:
        location = "None"
    if not user:
        user = "None"
    if not password:
        password = "None"
    if not token:
        token = "None"
    if install_cli:
        install_cli = "True"
    else:
        install_cli = "False"

    # go into the right directory to execute the script
    path = os.path.dirname(__file__)
    script = os.path.join(path, '../implementation/get_system/get/' + script)
    script += " " + url + \
              " " + location + \
              " " + user + \
              " " + password + \
              " " + token + \
              " " + install_cli

    # execute the script
    # status is the exit status code returned by the program
    status = os.system(script)
    if status != 0:
        raise Exception("Error occured in %s" % command.entry_point)
