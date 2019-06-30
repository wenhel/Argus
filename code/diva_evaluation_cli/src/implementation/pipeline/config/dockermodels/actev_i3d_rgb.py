import sys
import os
import pre_process_chunk
sys.path.insert(0, '../..')
from dummy_run import dummy_run
from diva_parameters import conf_dirs

def run(video,lock):
    DATA_DIR,CACHE_DIR,LOG_DIR,VIDEO_DIR,CHUNK_ID = pre_process_chunk.get_config_chunk()
    '''
        1. SET model, using the key provide in config.yaml -> pipeline
        2. SET directory, see config.yaml -> directory
        3. CONFIGURE parameters:
            {parameters,sub_parameters,nvidia_parameters}
        4. RUN
    '''

    # 1. SET dockermodel name, must be consistent with the name in config.yaml -> pipeline
    model_name = 'actev_i3d_rgb'

    # 2. SET directory information, must be consistent with the directories in config.yaml -> directory
    # VIDEO_DIR =conf_dirs.get('VIDEO_DIR')
    # DATA_DIR = conf_dirs.get('DATA_DIR')
    # OBJ_DIR = conf_dirs.get('OBJ_DIR')
    # DATA_DIR = '/results'

    # Create output dir
    # output_dir = os.sep.join([DATA_DIR, model_name, video])
    # if not os.path.exists(output_dir):
    #     os.makedirs(output_dir)

    # Create video list
    # lst_dir = os.sep.join([DATA_DIR, 'list'])
    # if not os.path.exists(lst_dir):
    #     os.makedirs(lst_dir)

    # tmp_lst = os.sep.join([DATA_DIR, str(video) + '.lst'])
    # if not os.path.exists(tmp_lst):
    #     with open(tmp_lst, 'w') as e:
    #         e.write(str(video) + '.mp4')
    #     e.close()


    # 3. CONFIGURE parameters. NOTICE: It will overwrite parameters in {dockermodel}.yaml
    # NV_PARAMETER = {'NV_GPU': "'%s'" % str(gid)}
    # PARAMETER = {'-p','8000:8000'} 
    PARA = {
        '--props_list_fn': '/result/actev_prop/%s/props_list.lst'%video,
        '--traj_img_root_path': '/result/actev_prop/%s/trajectory_images'%video,
        '--dst_feat_root_path': '/result/actev_i3d_rgb/%s'%video
    }
    
    str1 = '%s:%s:%s'%(DATA_DIR,'/result','rw')
    # str2 = '%s:%s'%(VIDEO_DIR,'/data/video')
    # str3 = '%s/%s:%s:%s'%(CACHE_DIR,model_name,'/tmp','rw')
    parameters = {
        'parameters':None,
        'nvidia_parameters':None,
        'sub_parameters' : PARA,
        'volume': { '-v':[str1] }
    }
    # 4. RUN
    print('run: PARA:%s'%str(parameters))
    success = dummy_run(video,model_name,lock,parameters)
    return success

def main():
    from multiprocessing import Lock
    lock = Lock()
    video = 'VIRAT_S_000000'
    success = run(video, lock)
    print success

if __name__ == '__main__':
    main()
