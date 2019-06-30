import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
sys.path.insert(0, '../..')
import diva_parameters
from diva_parameters import models, conf_log, conf_dirs, TEST, timestamp
import multiprocessing
# import diva_parallel
import time
import copy

def dummy_run(video,model_name,gid,PARA):
    '''
        1. GET model, using the key provided in config.yaml -> pipeline
        2. DEFINE directory, see config.yaml -> directory
        3. NEW video list with only one {video}
           (we keep the function of docker which can deal with multiple videos)
        4. INIT logger
        5. UPDATE parameters
        6. RUN
    '''
    model = models.get(model_name)
    model2 = copy.deepcopy(model)

    logger = diva_parameters.creat_diva_logger(video, model_name, conf_log)
    ## UPDATE parameters
    if PARA.get('parameters'):
        para = PARA.get('parameters')
        print('dummy:update parameters:%s\n' % para)
        model2.update_parameters(para)
        del para

    if PARA.get('volume'):
        para = PARA.get('volume')
        print('dummy:update volume:%s\n' % para)
        model2.update_volume(para)
        del para

    if PARA.get('sub_parameters'):
        para = PARA.get('sub_parameters')
        print('dummy:update sub_parameters:%s\n' % para)
        model2._parameters(para)

    if model2.type == 'nvidia_docker' :
        if not PARA.get('nvidia_parameters'):
            print('dummy:update nvidia_parameters:%s\n' % PARA.get('nvidia_parameters'))
            logger.logger.info('get_id:%d get!' % int(gid))
            NV_PARAMETER = {'NV_GPU': "'%s'" % str(gid)}
            print('dummy:gid_%d'%int(gid))
        else:
            NV_PARAMETER = PARA.get('nvidia_parameters')
        model2.update_nvidia_parameters(NV_PARAMETER)

    clean_vid = video.replace('.','_')
    model2.rename( clean_vid + '_' + model_name + '_' + timestamp)
    logger.logger.warn('model_%s:%s' % (model_name, model2.name))
    print('dummy:model.para:%s\n'%model2.cmd)
    

    start = time.time()
    if  TEST:
        success = model2.test(logger)
    else:
        success = model2.run(logger)

    end = time.time()
    logger.logger.warn('model_%s:%s, Time=%s, Success=%s' % 
        (model_name, model2.name, str(end-start), str(success)))
    return success
