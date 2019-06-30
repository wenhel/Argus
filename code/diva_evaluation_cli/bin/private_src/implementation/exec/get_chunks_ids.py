"""Exec module: utils

"""
import json
import sys

def get_chunks_ids(chunk_file, output):
    """ Get chunk ids from a chunk json file.

    Args:
        chunk_file (str): Path to a json chunk file
        output (str): Path to the output file containing chunk ids

    """
    chunk_ids = []
    chunks = json.load(open(chunk_file, 'r'))
    with open(output, "w") as f:
        for chunk_id in chunks:
            f.write(chunk_id + "\n")


if __name__ == '__main__':
    if len(sys.argv) == 3:
        get_chunks_ids(sys.argv[1], sys.argv[2])



