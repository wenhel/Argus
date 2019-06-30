# diva_parameters
import os
import sys
import time
import copy
from Dockermodel import Dockermodel
from DivaLogger import DivaLogger
import yaml
## all dockermodel yaml
import config.config_yaml
import pre_process_chunk
dockermodels, conf = config.config_yaml.init()
timestamp = str(int(time.time()))
DATA_DIR,CACHE_DIR,LOG_DIR,VIDEO_DIR,CHUNK_ID = pre_process_chunk.get_config_chunk()

## 1. log
conf_log = conf.get('log')
if conf_log.get('DB_CONFIG'):
    conf_log['DB_CONFIG']['dbname'] = conf_log.get('DB_CONFIG').get(
        'dbname', 'unkown_pipeline') + '_' + timestamp
    
## 2. FILE_CONFIG
conf['directory']['DATA_DIR']  = DATA_DIR
conf['directory']['VIDEO_DIR'] = VIDEO_DIR
conf['directory']['CACHE_DIR'] = CACHE_DIR
conf['directory']['LOG_DIR'] = LOG_DIR
conf_dirs = conf.get('directory')
## update log dir
if conf_log.get('FILE_CONFIG'):
    conf_log['FILE_CONFIG']['directory'] = os.path.join(LOG_DIR + '_' + timestamp)


## 3. dockermodels &  pipeline [only sequence-pipeline for now]
models = {}
prepipeline = conf.get('pipeline').get('preprocess')
if prepipeline:
    for dm_name in prepipeline:
        models[dm_name] = Dockermodel(dockermodels.get(dm_name), conf_log)
    del dm_name


pipename = conf.get('pipeline').get('name')
pipeline = conf.get('pipeline').get('sequence')
for dm_name in pipeline:
    models[dm_name] = Dockermodel(dockermodels.get(dm_name), conf_log)
del dm_name

## 5. parallel initialization
#PLL = conf.get('parallel')
GPUS = {v: False for v in conf.get('nvida_docker').get('NV_GPU')}
#WORKER_NUM = PLL.get('WORKER_NUM')
#real_WORKER_NUM = min(len(GPUS), WORKER_NUM)
#is_parallel = conf.get('pipeline').get('parallel')
is_parallel = True
## 6. test
#TEST = PLL.get('test')
TEST=False
## all dockermodels script
from config.dockermodels import *

# ------------------ ------------------ ------------------ ------------------ 

def init_models():
    '''pull model from private registry if not exist'''
    for model in models:
        if not model.exist():
            model.pull(REG_HOST)
    for pmodel in premodels:
        if not pmodel.exist():
            pmodel.pull(REG_HOST)
    return True


def init_dir():
    '''init local log dir'''
    full_log_path = conf_log['FILE_CONFIG']['directory']
    checkdir(full_log_path,'pre_out_dir',0)

def checkdir(ext_frames_dir, type_str, verbose=0):
    if not os.path.exists(ext_frames_dir):
        if verbose:
            sys.stderr.write("INIT: mkdir %r:%r\n" % (type_str, ext_frames_dir))
        os.makedirs(ext_frames_dir)
        return 1
    return 2

def dict2yaml(dict,out_dir,filename):
    out_full_file= os.path.join(out_dir,'%s.yaml'%filename)
    with open(out_full_file, 'w') as f:
        yaml.dump(dict, f)


def creat_diva_logger(vid, mid, config):
    '''create new logger only for diva project'''
    if not vid: vid = ''
    info = {'vid': vid, 'mid': mid}
    key = str(vid) + '_' + str(mid)

    if config.get('FLAG') == 'FILE':
        logfile = key + '.log'
        DATA_DIR = conf_dirs.get('DATA_DIR')
        config = copy.deepcopy(config)
        config.get('FILE_CONFIG').update({'filename': logfile})
        config.get('FILE_CONFIG').update({'name': 'diva_log_'+key})
        init_dir()
        logger = DivaLogger(config)
    elif config.get('FLAG') == 'DB':
        # update to VID + MID
        vidmid = key.replace('.', '_')
        config = copy.deepcopy(config)
        config.get('DB_CONFIG').update({'name': 'diva_log_'+ key})
        config.get('DB_CONFIG').update({'collection': vidmid})
        logger = DivaLogger(config)
    return logger
