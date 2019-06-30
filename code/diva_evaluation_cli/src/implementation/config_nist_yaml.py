# import yaml, 
import os, sys
import json,yaml

CURRENT_PATH = os.path.split(os.path.realpath(__file__))[0]
NIST_CONFIG_OUTDIR = os.path.join(CURRENT_PATH,'pipeline','config')

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
        #if flist is the empty list, return an empty list. This is arbitrary, if it turns out that
        #an empty dictionary is better, we can do something about that.
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

def yaml_load(filename):
	return merge([filename])

def init_parameters(FILE_INDEX,ACTIVITY_INDEX,CHUNK,VIDEO_LOCATION,SYSTEM_CACHE_DIRECTORY):

	conf = {
		'FILE_INDEX':FILE_INDEX,
		'ACTIVITY_INDEX':ACTIVITY_INDEX,
		'CHUNK':CHUNK,
		'VIDEO_DIR':VIDEO_LOCATION,
		'SYSTEM_CACHE_DIRECTORY':SYSTEM_CACHE_DIRECTORY,
		'NIST_CONFIG_OUTDIR':NIST_CONFIG_OUTDIR
		# 'DATA_DIR': os.path.join(SYSTEM_CACHE_DIRECTORY,'result')
		# 'LOG_DIR': os.path.join(SYSTEM_CACHE_DIRECTORY,'log')
	}
	out_file = os.path.join(NIST_CONFIG_OUTDIR,'config_nist.yaml')
	with open(out_file, 'w') as f:
		yaml.dump(conf,  f, default_flow_style=False)
	return True

# def init_dir(CHUNK,DATA_DIR):
	'''here CHUNK is actually the dir of all chunk.json'''
	# 1. get all chunk list
	# 2. build dirs with video.lst
	# return True

def get_config_nist():
    full_path = os.path.join(CURRENT_PATH,'pipeline','config','config_nist.yaml')
    config_nist = yaml_load(full_path)
    ACTIVITY_INDEX = config_nist.get('ACTIVITY_INDEX')
    FILE_INDEX = config_nist.get('FILE_INDEX')
    CHUNK = config_nist.get('CHUNK')
    # NIST_CONFIG_OUTDIR = config_nist.get('NIST_CONFIG_OUTDIR')
    SYSTEM_CACHE_DIRECTORY = config_nist.get('SYSTEM_CACHE_DIRECTORY')
    VIDEO_DIR = config_nist.get('VIDEO_DIR')
    return ACTIVITY_INDEX, FILE_INDEX,CHUNK,SYSTEM_CACHE_DIRECTORY,VIDEO_DIR



if __name__ == '__main__':
	FILE_INDEX=sys.argv[1]
	ACTIVITY_INDEX=sys.argv[2]
	CHUNK=sys.argv[3]
	VIDEO_LOCATION=sys.argv[4]
	SYSTEM_CACHE_DIRECTORY=sys.argv[5]
	init_parameters(FILE_INDEX,ACTIVITY_INDEX,CHUNK,VIDEO_LOCATION,SYSTEM_CACHE_DIRECTORY)


		# chunk_dict = json.load(open(CHUNK, 'r'))
	# for chunk_id, info in chunk_dict.items():
	# 	DATA_DIR = os.path.join(SYSTEM_CACHE_DIRECTORY,chunk_id)
 #    	if not os.path.exists(DATA_DIR):
 #        	os.makedirs(DATA_DIR)

	# 	video_lst = info.get(u'files')
	# 	for vid in video_lst:
	# 		tmp_list = DATA_DIR +'/%s.lst'%str(video)
	# 	    if not os.path.exists(tmp_list):
	# 	        with open(tmp_list, 'w') as e:
	# 	            e.write(str(video)+'\n')
	# 	            # print(str(video) + '.mp4')
	# 	        e.close()