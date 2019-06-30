#!/usr/bin/env python
import logging
from logging import FileHandler
from log4mongo.handlers import MongoHandler
import os


class DivaLogger():
    """
    DivaLogger
    """
    def __init__(self, conf_log):
        if isinstance(conf_log, dict):
            flag = conf_log.get('FLAG')
            if flag == 'DB':
                DB_CONFIG = conf_log.get('DB_CONFIG')
                logger = self.update_db_logger(DB_CONFIG)
            elif flag == 'FILE':

                FILE_CONFIG = conf_log.get('FILE_CONFIG')
                logger = self.update_file_logger(FILE_CONFIG)
            self.conf = conf_log
            self.logger = logger
            self.type = conf_log['FLAG']
        else:
            raise Exception("Can't configure log module from %s" % (conf_log))

    @property
    def conf(self):
        return self.conf

    @property
    def logger(self):
        return self.logger

    @property
    def type(self):
        return self.type

    def update_file_logger(self, FILE_CONFIG):
        ''' update_file_logger '''
        # FILE_CONFIG = conf_log.get('FILE_FONFIG')
        if FILE_CONFIG.get('directory') and FILE_CONFIG.get('filename'):
            logfile = os.sep.join(
                [FILE_CONFIG['directory'], FILE_CONFIG['filename']])
            flehandler = FileHandler(filename=logfile)
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')
            flehandler.setLevel(logging.DEBUG)
            logger = logging.getLogger(FILE_CONFIG['name'])
            logger.addHandler(flehandler)
            return logger
        else:
            raise Exception("Can't update file logger, wrong configure file")

    def update_db_logger(self, DB_CONFIG):
        ''' update_db_logger '''
        # DB_CONFIG = conf_log.get('DB_CONFIG')
        if DB_CONFIG.get('host') and DB_CONFIG.get('port'):
            mdbhandler = MongoHandler(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                database_name=DB_CONFIG.get('dbname', 'diva_pipeline_unknown'),
                collection=DB_CONFIG.get('collection', 'diva_db_unknown')
                )
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')
            mdbhandler.setLevel(logging.DEBUG)
            logger = logging.getLogger(DB_CONFIG['name'].replace('.', '_'))
            logger.addHandler(mdbhandler)
            return logger
        else:
            raise Exception("Can't update db logger, wrong configure file")

    def update_logger(self, config, info=None):
        ''' update_logger '''
        self.info = info
        conf = self.conf
        conf.update(config)
        if self.type == 'FILE':
            self.logger = self.update_file_logger(conf)
        elif self.type == 'DB':
            self.logger = self.update_db_logger(conf)
        else:
            raise Exception("Can't update non-type logger!")

    def test_logging(self, cmd):
        self.logger.warning(' '.join(cmd))

    def test_call_shell_logging(self, cmd, logger):
        from threading import Thread
        from subprocess import Popen, PIPE, STDOUT, CalledProcessError 
        import shlex
        import json

        def _consume_all( pipe, logger):
            '''pipe to logger all '''
            logger.info(json.loads(pipe.read()))

        def _call_shell(cmd,logger):    
            '''cmd to pipe'''
            print(' '.join(cmd))
            if not isinstance(cmd, list):
                logger.warning('callshell_logging:Exception: cmd must be a list')
                return False
            try:
                logger.warning('callshell:%s\n' % ' '.join(cmd))
                process = Popen(
                    shlex.split(' '.join(cmd)),
                    stdout=PIPE,
                    stderr=STDOUT,
                    bufsize=1
                )
                Thread(target=_consume_all, 
                       args=[process.stdout,logger]
                ).start()
                returncode = process.wait()
            except CalledProcessError as exception:
                logger.error('callshell_logging:Exception occured: ' +
                             str(exception))
                logger.error('callshell_logging failed\n')
                return False
            else:
                logger.warning('callshell: finished\n')
            return (returncode == 0)

        return _call_shell( cmd,logger)

def main():
    import sys
    import json
    from diva_parameters import conf_log
    log_dir = conf_log['FILE_CONFIG']['directory']
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    loggerx = DivaLogger(conf_log)

    # test logger
    SAMPLE_LOG = {
        'video': 'video_name_001',
        'module': 'module_name_001',
        'state': 'start',  # 2 is running, 0 is fail ,1 is success
        'extra': 'this is a logging test'
    }
    loggerx.logger.info(SAMPLE_LOG)

    # test call_shell_logging
    image = 'diva_preprocess:v1'
    cmd = ['docker', 'inspect', '--type=image'] + [image]
    success = loggerx.test_call_shell_logging(cmd, loggerx.logger)
    print(success)


if __name__ == '__main__':
    main()