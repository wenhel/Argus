"""Entry point module: merge-chunks

Implements the entry-point by using Python or any other languages.

"""
import argparse
import json

from diva_evaluation_cli.src.implementation.merge_chunks import merge_chunks

def entry_point(result_location, output_file, chunks_file, chunk_ids):
    """Method to complete: you have to raise an exception if an error occured in the program.

    Given a list of chunk ids, merges all the chunks system output present in the list.

    Args:
        result_location (str): Path to get the result of the chunks processing
        chunk_file (str):  Path to directory where intermediate system output is stored
        output_file (str): Path to the output file generated
        chunk_ids (:obj:`list`): List of chunk ids

    """
    merge_chunks(result_location, output_file, chunks_file, chunk_ids)
