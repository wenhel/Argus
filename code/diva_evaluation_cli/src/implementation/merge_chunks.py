"""Merge chunk source code

"""
import json
import os
import re

def merge_chunks(result_location, output_file, chunks_file, chunk_ids=None):
    """Merge a list of chunk results files inside an output file, and a chunks file.

    Args:
        result_location (str): Path to chunk results files
        output_file (str): Path to output file where chunks are merged
        chunks_file (str): Path to a global chunk file created after merging
        chunk_ids (:obj: `list`, optional): List of chunk ids to merge, if empty, merge every chunk results files

    """
    output_dict = {"filesProcessed": [], "activities": []}
    chunks_dict = {}

    ## 1. get chunk_files--> paths
    chunk_files = []
    if chunk_ids == None:
        # Find all the chunks
        chunk_files = get_chunk_files("Chunk", result_location)
    else:
        # Find the specified chunk file
        for chunk_id in chunk_ids:
            chunk_files.extend(get_chunk_files(chunk_id, result_location))

    ## 2. load and deal with result by each chunk
    for chunk_file in chunk_files:
        chunk = json.load(open(chunk_file, 'r'))

        # Remove out_of_bounds activities --> we do not have this "out_of_bounds"
        activities_clean = []
        for activity in chunk["activities"]:
            if activity["activity"] != "out_of_bounds":
                activities_clean.append(activity)

        # Generate output_file
        output_dict["activities"].extend(activities_clean)
        for file_name in chunk["filesProcessed"]:
            if file_name not in output_dict["filesProcessed"]:
                output_dict["filesProcessed"].append(file_name)

        # Generate chunks_file
        chunk_key = re.search('(Chunk[0-9]+)', chunk_file).group(1)
        chunks_dict[chunk_key] = {}
        activities = []
        for activity in activities_clean:
            if activity["activity"] not in activities:
                activities.append(activity["activity"])
        chunks_dict[chunk_key].update({"activities": activities, "files": chunk["filesProcessed"]})

    with open(output_file, 'w') as f:
        json.dump(output_dict, f, indent=2)

    with open(chunks_file, 'w') as f:
        json.dump(chunks_dict, f, indent=2)

def get_chunk_files(chunk_id, result_location):
    """Get a chunk results file according to a given chunk id and a result location

    Args:
        chunk_id (str): Chunk id
        result_location (str): Path to chunk results files
    """
    chunk_files = []
    for chunk_file in os.listdir(result_location):
        if chunk_id in chunk_file and chunk_file.endswith('.json'):
            chunk_files.append(os.path.join(result_location, chunk_file))
    # print('Merge-chunks: result_location:%s,output_file:%s,chunks_file:%s,chunk_ids:%s'%(result_location, output_file, chunks_file, chunk_ids))
    print('Merge-chunks: get_chunk_files... chunk_id=%s, list=%s\n'%(str(chunk_id),str(chunk_files)))
    return chunk_files
