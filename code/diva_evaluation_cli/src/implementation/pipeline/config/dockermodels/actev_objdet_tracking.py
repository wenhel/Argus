import sys
import os
import pre_process_chunk
sys.path.insert(0, '../..')
from dummy_run import dummy_run
import diva_parameters
from diva_parameters import conf_dirs
from diva_parameters import models

def run(video,gid):
    DATA_DIR,CACHE_DIR,LOG_DIR,VIDEO_DIR,CHUNK_ID = pre_process_chunk.get_config_chunk()

    '''
        1. SET model, using the key provide in config.yaml -> pipeline
        2. SET directory, see config.yaml -> directory
        3. CONFIGURE parameters:
            {parameters,sub_parameters,nvidia_parameters}
        4. RUN
    '''
    # lock.acquire()
    # 1. SET dockermodel name, must be consistent with the name in config.yaml -> pipeline
    model_name = 'actev_objdet_tracking'

    # 2. SET directory information, must be consistent with the directories in config.yaml -> directory
    # OBJ_DIR = conf_dirs.get('OBJ_DIR')
    # VIDEO_DIR =conf_dirs.get('VIDEO_DIR')
    # DATA_DIR = conf_dirs.get('DATA_DIR')

    # Create output dir
    output_dir = os.sep.join([DATA_DIR, 'actev_obj_det', str(video)])
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_dir1 = os.sep.join([DATA_DIR, 'actev_tracking', str(video)])
    if not os.path.exists(output_dir1):
        os.makedirs(output_dir1)

    # Create video list
    with open(os.sep.join([DATA_DIR, str(video) + '.lst']), 'w') as e:
        # e.write(str(video) + '.mp4')
        e.write(str(video))
    e.close()


    # 3. CONFIGURE parameters. NOTICE: It will overwrite parameters in {dockermodel}.yaml
    # NV_PARAMETER = {'NV_GPU': "'%s'" % str(gid)}
    # PARAMETER = {'-p','8000:8000'} 
    PARA = {	
	'--frame_gap':30,
        '--threshold_conf': '0.0001',
	'--video_dir': '/data/video',
        '--video_lst_file': os.sep.join(['/result', str(video) + '.lst']),
        '--out_dir': '/result/actev_obj_det',
	'--get_tracking':' ',
	'--tracking_dir': '/result/actev_tracking', 
    }
    
    str1 = '%s:%s:%s'%(DATA_DIR,'/result','rw')
    str2 = '%s:%s'%(VIDEO_DIR,'/data/video')
    str3 = '%s/%s:%s:%s'%(CACHE_DIR,model_name,'/tmp','rw')
    parameters = {
        'parameters':None,
        'nvidia_parameters':None,
        'sub_parameters' : PARA,
        'volume': { '-v':[str1,str2,str3] }
    }
    # 4. RUN
    # model = models.get(model_name)
    print('run: PARA:%s'%str(parameters))
    success = dummy_run(video,model_name,gid,parameters)
    # lock.release()
    return success

def main():
    from multiprocessing import Lock
    lock = Lock()
    video = 'VIRAT_S_000000.mp4'
    success = run(video, lock)
    print success

if __name__ == '__main__':
    main()
