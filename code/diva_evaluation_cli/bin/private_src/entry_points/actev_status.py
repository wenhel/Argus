"""Entry point module: status

This file should not be modified.
"""
import os

from diva_evaluation_cli.bin.private_src.implementation.status.check_status import check_status

def entry_point(query_type, chunk_id=None):
    """Private entry point.

    Get the status of a chunk id

    Args:
        query_type (str): status type desired
        chunk_id (str, optional): chunk id
    """
    check_status(query_type, chunk_id=chunk_id)


