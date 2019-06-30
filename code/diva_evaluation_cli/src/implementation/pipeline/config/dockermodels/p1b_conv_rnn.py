import sys
import os
import pre_process_chunk
sys.path.insert(0, '../..')
from dummy_run import dummy_run
from diva_parameters import conf_dirs

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
    model_name = 'p1b_conv_rnn'

    # 2. SET directory information, must be consistent with the directories in config.yaml -> directory
    # VIDEO_DIR = conf_dirs.get('VIDEO_DIR')
    # DATA_DIR = conf_dirs.get('DATA_DIR')
    # CACHE_DIR = conf_dirs.get('CACHE_DIR')

    # Create output dir
    cache_dir = os.sep.join([CACHE_DIR, model_name, video])
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # Create output dir ## all results in one directory
    output_dir = os.sep.join([DATA_DIR, model_name])
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create video list
    tmp_list = DATA_DIR +'/%s.lst'%str(video)
    if not os.path.exists(tmp_list):
        with open(tmp_list, 'w') as e:
            e.write(str(video)+'\n')
            # print(str(video) + '.mp4')
        e.close()

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
        '--feature_dir': '/result/actev_i3d_rgb/%s'%str(video),
        '--anno_dir': '/result/actev_prop/%s/annotations/'%str(video),
        '--video_lst_file': '/result/%s.lst'%str(video),
        '--tmp_dir': '/tmp/%s'%str(video),
        '--out_dir': '/result/%s'%model_name
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
    # parameters = {
    #      'parameters':{ 
    #             '-v': '%s:%s:%s'%(DATA_DIR,'/result','rw'),
    #             '-v': '%s:%s'%(VIDEO_DIR,'/data/video'),
    #             '-v': '%s/%s:%s:%s'%(CACHE_DIR,model_name,'/tmp','rw'),
    #         },
    #     'nvidia_parameters':None,
    #     'sub_parameters' : PARA
    # }
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
            'sub_parameters' : {'-rf': '/tmp2/%s'%str(video)},
            'nvidia_parameters':None,
        }
        rm_success = dummy_run(video,model_name2,lock,parameters2)
        # docker run --rm --name $docker_name --entrypoint /bin/rm \
        # -v /tmp/$vid:/tmp2:rw actev_ubuntu:v1  -rf /tmp2/$vid.mp4
    return success and rm_success

def main():
    from multiprocessing import Lock
    lock = Lock()
    video = 'VIRAT_S_000000'
    success = run(video, lock)
    print success

if __name__ == '__main__':
    main()
