"""Entry point module: validate-system

This file should not be modified.
"""
import os
from diva_evaluation_cli.bin.private_src.implementation.validate_system.validate_system import validate_system

def entry_point():
    """Private entry point.

    Checks the structure of the  directory after ActEV-system-setup is run. Checks for expected API contents, etc.

    """
    validate_system()

