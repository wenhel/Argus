import sys
import os
import pre_process_chunk
sys.path.insert(0, '../..')
from dummy_run import dummy_run
from diva_parameters import conf_dirs
# import shutil
DATA_DIR,CACHE_DIR,LOG_DIR,VIDEO_DIR,CHUNK_ID = pre_process_chunk.get_config_chunk()
def run(video,lock):
    '''
        1. SET model, using the key provide in config.yaml -> pipeline
        2. SET directory, see config.yaml -> directory
        3. CONFIGURE parameters:
            {parameters,sub_parameters,nvidia_parameters}
        4. RUN
    '''

    # 1. SET dockermodel name, must be consistent with the name in config.yaml -> pipeline
    model_name = 'actev_prop'

    # 2. SET directory information, must be consistent with the directories in config.yaml -> directory
    # VIDEO_DIR =conf_dirs.get('VIDEO_DIR')
    # DATA_DIR = conf_dirs.get('DATA_DIR')
    # CACHE_DIR =  conf_dirs.get('CACHE_DIR')

    # Create output dir
    # output_dir = os.sep.join([DATA_DIR, model_name, video])
    # if not os.path.exists(output_dir):
    #     os.makedirs(output_dir)

    # Create video list
    tmp_list = DATA_DIR +'/%s.lst'%str(video)
    if not os.path.exists(tmp_list):
        with open(tmp_list, 'w') as e:
            e.write(str(video))
        e.close()

    ## Create cache dir
    cache_dir = os.sep.join([CACHE_DIR, model_name, video])
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # trim tacking result
    # video_trim = os.path.splitext(str(video))[0]
    # person_path = os.path.join(DATA_DIR,'actev_tracking',str(video),'Person')
    # vehicle_path = os.path.join(DATA_DIR,'actev_tracking',str(video),'Vehicle')
    # os.rename(os.path.join(person_path,'%s.txt'%str(video)),os.path.join(person_path,'%s.txt'%video_trim))
    # os.rename(os.path.join(vehicle_path,'%s.txt'%str(video)),os.path.join(vehicle_path,'%s.txt'%video_trim))

    # 3. CONFIGURE parameters. NOTICE: It will overwrite parameters in {dockermodel}.yaml
    # NV_PARAMETER = {'NV_GPU': "'%s'" % str(gid)}
    # PARAMETER = {'-p','8000:8000'} 
    PARA = {
        '--video_list_fn': '/result/%s.lst'%str(video),
        '--tracklet_root_path': '/result/actev_tracking/%s'%str(video),
        '--anno_root_path': '/result/actev_prop/%s/annotations/'%str(video),
        '--traj_img_root_path': '/result/actev_prop/%s/trajectory_images/'%str(video),
        '--props_list_fn': '/result/actev_prop/%s/props_list.lst'%str(video),
        '--tmp_root_path': '/tmp/%s'%str(video)
    }
    
    # parameters = {
    #     'parameters':{ 
    #             '-v': '%s:%s:%s'%(DATA_DIR,'/result','rw'),
    #             '-v': '%s:%s'%(VIDEO_DIR,'/data/video'),
    #             '-v': '%s/%s:%s:%s'%(CACHE_DIR,model_name,'/tmp','rw')
    #         },
    #     'nvidia_parameters':None,
    #     'sub_parameters' : PARA
    # }
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
    success = dummy_run(video,model_name,lock,parameters)
    if success:
        ## rm tmp_file
        model_name2 = 'actev_ubuntu'
        parameters2 = {
            'parameters':{
                '--entrypoint': '/bin/rm',
                '-v': '%s/%s:%s:%s'%(CACHE_DIR,model_name,'/tmp2','rw')
            },
            'nvidia_parameters':None,
            'sub_parameters' : {'-rf': '/tmp2/%s'%str(video)}
        }
        rm_success = dummy_run(video,model_name2,lock,parameters2)
    # docker exec 765511b2869e sh -c 'rm -rf /backup/*.zip'
    # shutil.rmtree(cache_dir, ignore_errors=True)
    return success and rm_success

def main():
    from multiprocessing import Lock
    lock = Lock()
    video = 'VIRAT_S_000000'
    success = run(video, lock)
    print success

if __name__ == '__main__':
    main()
