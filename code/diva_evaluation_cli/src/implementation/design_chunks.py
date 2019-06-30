"""Design chunks source code

"""
import json

def design_chunks(file_index_file, activity_index_file, save_path, num_videos_per_chunk=4):
    """  Merge file_index with activity_index content into different chunks written in a file

    Args:
        file_index_file (str):       Path to file index json file
        activity_index_file (str):   Path to activity index json file
        save_path (str):             Path to save chunks file
        num_videos_per_chunks(int):  number of videos in a chunk
    """
    file_index = json.load(open(file_index_file, 'r'))
    activity_index = json.load(open(activity_index_file, 'r'))
    chunk_dict = {}
    chunk_count = 0
    chunk_prefix = "Chunk"
    all_activities = list(activity_index.keys())

    for index, file_name in enumerate(file_index.keys()):
        if index % num_videos_per_chunk == 0:
            # start a new chunk
            chunk_count += 1
            chunk_name = chunk_prefix + str(chunk_count)
            chunk_dict[chunk_name] = {"activities": all_activities, 
                                    "files": []}
        chunk_name = chunk_prefix + str(chunk_count)
        chunk_dict[chunk_name]["files"].append(file_name)
    with open(save_path, 'w') as f:
        json.dump(chunk_dict, f, indent=2)


if __name__ == '__main__':
    file_index_file=sys.argv[1]
    activity_index_file=sys.argv[2]
    save_path=sys.argv[3] ## this is dir + name
    num_videos_per_chunk=int(sys.argv[4])
    design_chunks(file_index_file, activity_index_file, save_path, num_videos_per_chunk)