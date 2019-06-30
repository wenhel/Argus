# preprocess_chunk.py

import os
import sys
import yaml,json
import config_nist_yaml
CURRENT_PATH = os.path.split(os.path.realpath(__file__))[0]
ACTIVITY_INDEX, FILE_INDEX,CHUNK,SYSTEM_CACHE_DIRECTORY,VIDEO_DIR = config_nist_yaml.get_config_nist()

def init_dir(chunk_id,chunk_json):
    DATA_DIR = os.path.join(SYSTEM_CACHE_DIRECTORY,chunk_id)
    LOG_DIR = os.path.join(DATA_DIR,'log')
    CACHE_DIR = os.path.join(DATA_DIR,'cache')
    checkdir(DATA_DIR, 'full_res_dir', 0)
    checkdir(LOG_DIR, 'full_log_dir', 0)
    checkdir(CACHE_DIR, 'full_log_dir', 0)
    

    chunk_dict = json_load(chunk_json)
    chunk_dict_i = chunk_dict.get(chunk_id)
    video_lst_fn = chunk_dict_i.get('files')
    slpit_video_lst(DATA_DIR,video_lst_fn)
    whole_video_lst(DATA_DIR,chunk_id,video_lst_fn)
    return DATA_DIR, CACHE_DIR, LOG_DIR


def init_chunk_config(chunk_id,chunk_json,res_dir):
    DATA_DIR, CACHE_DIR, LOG_DIR = init_dir(chunk_id,chunk_json)
    out_dict = {
        'DATA_DIR' : DATA_DIR,
        'CACHE_DIR' : CACHE_DIR,
        'LOG_DIR' : LOG_DIR,
        'VIDEO_DIR' : VIDEO_DIR,
        'CHUNK_ID':chunk_id
    }
    full_filename = os.path.join(SYSTEM_CACHE_DIRECTORY,'config_chunk.yaml')
    yaml_save(out_dict,full_filename)


def do_job(chunk_id):
    config_nist_fn = os.path.join(CURRENT_PATH,'config','config_nist.yaml')
    config_nist = yaml_load(config_nist_fn)
    if not CHUNK:
        print('There is no available chunk.json')
        return 
    chunk_dict = json_load(CHUNK)
    if not chunk_dict.has_key(chunk_id):
        print('There is no available chunk_id %s'%chunk_id)
        return 
    init_chunk_config(chunk_id,CHUNK,SYSTEM_CACHE_DIRECTORY)

def get_config_chunk():
    full_filename = os.path.join(SYSTEM_CACHE_DIRECTORY,'config_chunk.yaml')
    config_chunk_dict =  yaml_load(full_filename)
    DATA_DIR = config_chunk_dict.get('DATA_DIR')
    CACHE_DIR = config_chunk_dict.get('CACHE_DIR')
    LOG_DIR = config_chunk_dict.get('LOG_DIR')
    VIDEO_DIR = config_chunk_dict.get('VIDEO_DIR')
    CHUNK_ID = config_chunk_dict.get('CHUNK_ID')
    return DATA_DIR,CACHE_DIR,LOG_DIR,VIDEO_DIR,CHUNK_ID

def merge(fList):
    ''' 
    Takes a list of yaml files and loads them as a single yaml document.
    Restrictions:
    1) None of the files may have a yaml document marker (---)
    2) All of the files must have the same top-level type (dictionary or list)
    3) If any pointers cross between files, then the file in which they are defined (&) must be 
    earlier in the list than any uses (*).
    '''
    if not fList:
        return []
    sList = []
    for f in fList:
        with open(f, 'r') as stream:
            sList.append(stream.read())
    fString = ''
    for s in sList:
        fString = fString + '\n' + s
    y = yaml.load(fString)
    return y

def slpit_video_lst(full_res_dir,video_lst):
    # videolist = init_videos_from_lst(video_lst_file)
    for video in video_lst:
        with open(os.sep.join([full_res_dir, str(video) + '.lst']), 'w') as e:
            e.write(str(video)+'\n')
        e.close()

def whole_video_lst(full_res_dir,chunk_id,video_lst):
        with open(os.sep.join([full_res_dir, chunk_id + '.lst']), 'w') as e:
            for video in video_lst:
                e.write(str(video)+'\n')
        e.close()

def checkdir(ext_frames_dir, type_str, verbose=0):
    if not os.path.exists(ext_frames_dir):
        if verbose:
            sys.stderr.write("INIT: mkdir %r:%r\n" % (type_str, ext_frames_dir))
        os.makedirs(ext_frames_dir)
        return 1
    return 2


def yaml_load(filename):
    return merge([filename])


def yaml_save(data_dict,full_filename):
    with open(full_filename, 'w') as outfile:
        yaml.dump(data_dict, outfile) # default_flow_style=False

def json_load(full_filename):
    return json.load(open(full_filename, 'r'))


if __name__ == '__main__':
    chunk_id=sys.argv[1]
    do_job(chunk_id)
