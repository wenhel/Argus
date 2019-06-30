## demo for diva_pipline
## version: v2
## last modified 2017.10.06

import time
import os
import config
import diva_parameters
from diva_parameters import models, prepipeline, pipeline, pipename,is_parallel
from diva_parameters import GPUS, conf, timestamp
import pre_process_chunk 
import merge_inner_chunk
import config_nist_yaml
DATA_DIR,CACHE_DIR,LOG_DIR,VIDEO_DIR,CHUNK_ID = pre_process_chunk.get_config_chunk()
ACTIVITY_INDEX, FILE_INDEX,CHUNK,SYSTEM_CACHE_DIRECTORY,VIDEO_DIR = config_nist_yaml.get_config_nist()

## for parallel computation
from multiprocessing import Queue,Process


def init_prepipeline(videolist):
    '''pre-pipline, run web/ui dockermodels'''
    success = True
    DATA_DIR = diva_parameters.conf_dirs.get('DATA_DIR')
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    ## for log dir
    diva_parameters.init_dir()
    return success


def pos_init_prepipeline():
    '''Clean docker containers'''
    success = True
    for pi in prepipeline:
        model = models[pi]
        if not model.exist():
            print('posprocess_prepipeline:docker-img not exist: %s' % pi)
            continue
        if model.status():
            success = model.stop()
            print('posprocess_prepipeline:docker-img running -> stop: %s' % pi)
            continue
    return success

def post_pipeline(DATA_DIR,video_lst_file,out_file):
    '''merge results inside a CHUNK'''
    sucess = False
    actev_conv_rnn_dir = os.path.join( DATA_DIR,'actev_conv_rnn')
    p1b_conv_rnn_dir = os.path.join( DATA_DIR,'p1b_conv_rnn')
    if not (os.path.exists(actev_conv_rnn_dir)
            and os.path.exists(p1b_conv_rnn_dir)
            ):
        print('warn: one or more related dirs do not exist')
        return sucess
    
    sucess = merge_inner_chunk.inner_merge(video_lst_file,
        actev_conv_rnn_dir,p1b_conv_rnn_dir,out_file)
    return sucess

def do_job_parallel_gpu_qu(videolist):
    def init_queue(queue,GPULST):
        for  i in  GPULST:
            queue.put(i)
        return queue

    def do_job_single(video,gpu_id,queue):
        ''' single job with gpu '''
        sucess = True
        for mid in pipeline:
            print('vid:%s, mid:%s, GPUS=%s' % (video, mid, str(queue.qsize())))
            info = {
                'extra_info': pipename + '_' + timestamp,
                'module_name': mid,
                'status': 'start',
                'video_name': video
            }
            model = eval('config.dockermodels.' + mid)
            success = model.run(video,gpu_id)
            print('model=%s,sucess=%s\n'%(str(mid),str(sucess)))
            if not success:
                info['status'] = 'fail'
                break
            else:
                info['status'] = 'succeed'
            print(info)
        queue.put(gpu_id)

    GPULST = GPUS.keys() ## GPULST = range()
    queue = Queue()
    queue = init_queue(queue, GPULST)
    tasks = []
    for vid in videolist:
        gpu_id = queue.get()
        taski = Process(target=do_job_single,args=(vid,gpu_id,queue))
        taski.start()
        tasks.append(taski)
    for taski in tasks :
        taski.join()
    

def do_job_loop(videolist):
    results = []
    print('do_job_loop:' + results)
    for video in videolist:
        success = None
        try:
           success =  do_job_single(video)
           if not success:
                print('do_job_loop: fail on video %s' + video)
        except CalledProcessError as exception:
            print('do_job_loop: error on video %s' + video) 
        results.append(success)
    print('do_job_loop:' + results)
    return results


def init_videos_from_lst(video_lst_file):
    videolist = []
    vlf = open(video_lst_file)
    for line in vlf.readlines():
        name = line.split('\n')[0]
        videolist.append(name)
    vlf.close()
    return videolist


def main(chunk_id,out_file=None):
    chunk_id = CHUNK_ID 
    if not out_file:
        out_file = os.path.join(SYSTEM_CACHE_DIRECTORY,'out_%s.json')%CHUNK_ID
    pre_process_chunk.do_job(chunk_id)
    print(diva_parameters.conf_dirs)
    print('Process:MAIN:PID:%d' % os.getpid())
    ## GET video_lst_file from configure
    video_lst_file = os.path.join(DATA_DIR, chunk_id + '.lst')
    videolist = init_videos_from_lst(video_lst_file)
    init_success = init_prepipeline(videolist)
    if init_success:
        time.sleep(3)## for system initialization
        if is_parallel:
            print("it is parallel with merge...")
            result_list = do_job_parallel_gpu_qu(videolist)
            sucess = post_pipeline(DATA_DIR,video_lst_file,out_file)
        else:
            result_list = do_job_loop(videolist)
        print("result_list: %s"%str(result_list))
    pos_success = pos_init_prepipeline()
    print("postprocess: %s"%str(pos_success))
    return result_list
