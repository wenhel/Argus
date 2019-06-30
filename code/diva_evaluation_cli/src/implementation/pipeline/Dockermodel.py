#!/usr/bin/python
# Filename: Dockermodel.py

import shlex
import os
from DivaLogger import DivaLogger
from subprocess import Popen, PIPE, STDOUT, CalledProcessError


class Dockermodel():
    """
    DOCKERMODEL
    """
    def __init__(self, attrs, log):
        if isinstance(attrs, dict):
            self.attrs = attrs
            if self.attrs.get('name') is None:
                self.attrs['name'] = self.attrs['image']  
        else:
            raise Exception("Can't create module from %s" % (attrs))

        if isinstance(log, dict):
            self.log = log
        else:
            raise Exception("Can't configure log module from %s" % (log))

    @property
    def name(self):
        if self.attrs.get('name') is not None:
            return self.attrs['name']
        else:
            return None

    @property
    def type(self):
        if self.attrs.get('type') is not None:
            return self.attrs['type']
        else:
            return None

    @property
    def volume(self):
        if self.attrs.get('volume') is not None:
            return self.attrs['volume']
        else:
            return None

    def update_volume(self,other):
        self.attrs['volume'] = other

    @property
    def option(self):
        if self.attrs.get('option') is not None:
            return self.attrs['option']
        else:
            return None

    @property
    def image(self):
        if self.attrs.get('image') is not None:
            return self.attrs['image'] + ':' + self.attrs['tag']
        else:
            return None

    @property
    def parameters(self):
        if self.attrs.get('parameters') is not None:
            return self.attrs['parameters']
        else:
            return None

    @property
    def sub_parameters(self):
        '''
        sub_parameters are parameters for inner-docker functions.
        '''
        if self.attrs.get('sub_parameters') is not None:
            return self.attrs['sub_parameters']
        else:
            return None

    @property
    def nvidia_parameters(self):
        '''
        nvidia_parameter are parameters for nvidia_docker.
        '''
        if self.attrs.get('nvidia_parameters') is not None:
            return self.attrs['nvidia_parameters']
        else:
            return None

    @property
    def log(self):
        if self.log is not None:
            return self.log
        else:
            return None

    @property
    def cmd(self):
        '''parser the cmd'''
        cmd = self._update_cmd()
        return cmd
    
    def _update_cmd(self):
        if self.type == 'docker':
            prefix = [self.type, 'run']
        elif self.type == 'nvidia_docker':
            nvidia_parameterx = '='.join(
                self._para2cmdstr(self.nvidia_parameters))
            prefix = [nvidia_parameterx, 'nvidia-docker', 'run']
        else:
            raise Exception("Can't run %s, error in type" % self.name)
        name = ['--name', self.name]
        cmd = prefix + self.option + name + self._para2cmd(
            self.parameters) + self._para2cmd(self.volume) + [
                self.image
            ] + self._para2cmd(self.sub_parameters)
        self.cmd = cmd
        return cmd

    def update_nvidia_parameters(self, other):
        '''update n_para'''
        if not isinstance(other, dict):
            Exception("Can't _parameter %s " % (self.name))
            return False
        elif self.attrs.get('nvidia_parameters') is not None:
            self.attrs['nvidia_parameters'].update(other)
        else:
            self.attrs['nvidia_parameters'] = other
        self._update_cmd()
        # print('update_nvidia_parameters:%s'%self.cmd)
        return True
    
    def _parameters(self, other):
        '''update sub_para, which is para of scripts in docker'''
        if not isinstance(other, dict):
            Exception("Can't _parameter %s " % (self.name))
            return False
        elif self.attrs.get('sub_parameters') is not None:
            self.attrs['sub_parameters'].update(other)
        else:
            self.attrs['sub_parameters'] = other
        self._update_cmd()
        # print('_parameters:%s\n\n'%self.cmd)
        return True

    def update_parameters(self, other):
        '''update docker para'''
        if not isinstance(other, dict):
            Exception("Can't update_parameter %s " % (self.name))
            return False
        elif self.attrs.get('parameters') is not None:
            self.attrs['parameters'].update(other)
        else:
            self.attrs['parameters'] = other
        self._update_cmd()
        return True

    def rename(self, other):
        '''rename the container of a docker image'''
        if self.attrs.get('name') is not None:
            self.attrs['name'] = other
        else:
            self.attrs['name'] = other
        self._update_cmd()

    def update_log(self, other):
        '''
        Update log. must have the keys {FLAG, FILE_CONFIG, DB_CONFIG} 
        '''
        if self.log is not None:
            self.log.update(other)
        else:
            self.log = other

    # ------------ ------------ ------------ ------------ ------------ ------------ 
    def run(self, logger=None, cmd=None):
        '''docker run'''
        self._update_cmd()
        if logger is None:
            logger = DivaLogger(self.log)
        if cmd is None:
            cmd = self.cmd
        success = self._call_shell_logging(cmd, logger)
        # print('self.cmd = %s'%self.attrs)
        return success

    def test(self, logger=None):
        '''testing the cmd'''
        self._update_cmd()
        if logger is None:
            logger = DivaLogger(self.log)
        logger.test_logging(self.cmd)
        # print('self.cmd = %s'%self.cmd)
        return True

    def pull(self, registry_host, logger=None):
        '''docker pull'''
        if logger is None:
            logger = DivaLogger(self.log)
        rc2 = 1
        cmd = ['docker', 'pull', os.sep.join([registry_host, self.image])]
        rc1, _, _ = self._callshelldirct(cmd, logger)
        if rc1 == 0:
            cmd2 = [
                'docker', 'tag', os.sep.join([registry_host, self.image]),
                self.image
            ]
            rc2, _, _ = self._callshelldirct(cmd2, logger)
        if rc2 == 0:
            return True
        return False

    def exist(self, logger=None):
        '''check docker image existence'''
        if logger is None:
            logger = DivaLogger(self.log)
        cmd = ['docker', 'inspect', '--type=image'] + [self.image]
        rc, _, _ = self._callshelldirct(cmd, logger)
        if rc == 1:
            return False
        return True

    def stop(self, logger=None):
        '''check docker image existence'''
        if logger is None:
            logger = DivaLogger(self.log)
        cmd = ['docker', 'stop'] + [self.name]
        rc, _, _ = self._callshelldirct(cmd, logger)
        if rc == 1:
            return False
        return True    

    def status(self, logger=None):
        '''
        check status of an container 
        rc=0 and false => there is container but not running
        rc=0 and true => there is container and running
        rc=1 and '' => there is no container
        '''
        if logger is None:
            logger = DivaLogger(self.log)  
        cmd1 = ['docker','container', 'inspect'] + [self.name]
        rc1, _, _ = self._callshelldirct(cmd1, logger) 
        if rc1==1:
            logger.logger.warn('status:container not exist:%s'%self.name)
            return False 
        cmd = ['docker','container', 'inspect', '-f', '{{.State.Running}}'] + [self.name]
        rc, stdout, _ = self._callshelldirct(cmd, logger)  # rc = 0 if true
        # print('cmd=%s rc:%s, stdout:%s'%(cmd,str(rc),stdout.strip('\n').lower()))
        return stdout.strip('\n').lower() in ("true") and rc == 0

    def _call_shell_logging(self, cmd, divalogger):
        '''
        cmd to pipe
        '''
        logger = divalogger.logger
        if not isinstance(cmd, list):
            logger.warn('callshell_logging:Exception: cmd must be a list')
            return False
        try:
            logger.warn('callshell:%s' % ' '.join(cmd))
            process = Popen(
                ' '.join(cmd),
                stdout=PIPE,
                stderr=STDOUT,
                shell=True,
                universal_newlines=True,
                bufsize=20)
            while True:
                line = process.stdout.readline().decode()
                logger.warn(line)
                if not line:
                    break
            returncode = process.wait()
        except CalledProcessError as exception:
            logger.error('callshell_logging:Exception occured: ' +
                         str(exception))
            logger.error('callshell_logging failed')
            return False
        else:
            logger.warn('callshell: finished')
        return (returncode == 0)

    def _callshelldirct(self, cmd, divalogger):
        '''
        directly call shell cmd without logging
        '''
        logger = divalogger.logger
        if isinstance(cmd, list):
            logger.info('_callshelldirct:%s' % ' '.join(cmd))
            try:
                proc = Popen(
                    ' '.join(cmd),
                    # shlex.split(' '.join(cmd)),
                    stdout=PIPE,
                    stderr=STDOUT,
                    shell=True,
                    universal_newlines=True)
                stdout, stderr = proc.communicate()
                exitcode = proc.returncode
                proc.wait()
                logger.info('_callshelldirct:Return:%s' % str(exitcode))
            except CalledProcessError as exception:
                logger.error('_callshelldirct:Exception occured: ' +
                            str(exception))
                return False
            else:
                logger.info('_callshelldirct: Finished')
        else:
            logger.error(
                '_callshelldirct: Exception occured: cmd must be a list')
            return False
        return exitcode, stdout, stderr

    def _para2cmd(self, para):
        '''
         para is a dict
        '''
        cmd = []
        if not para:
            return cmd
        else:
            if para.has_key('python'):
                    cmd.extend(['python', para.get('python')])
            if para.has_key('--entrypoint'):
                    cmd.extend(['--entrypoint', para.get('--entrypoint')])
            for k, v in para.items():
                if v == 'Null' or k=='python' or k=='--entrypoint':
                    continue
                if isinstance(v, list):
                    for vi in v:
                        cmd.extend([str(k), str(vi)])
                else:
                    cmd.extend([str(k), str(v)])
        return cmd

    def _para2cmdstr(self, para):
        '''
        para is a dict for nvidia parameters
        '''
        cmd = []
        if not para:
            return cmd
        else:
            for k, v in para.items():
                if v == 'Null':
                    continue
                if isinstance(v, list):
                    # print(v)
                    for vi in v:
                        cmd.extend([str(k), "'%s'" % str(vi)])
                else:
                    cmd.extend([str(k), "'%s'" % str(v)])
        return cmd


def main():
    from multiprocessing import Lock
    lock = Lock()
    video = 'MCTTR0101a.mov.deint'
    from config.dockermodels import diva_preprocess
    diva_preprocess.run(video, lock)
    from config.dockermodels import diva_persondetect
    diva_persondetect.run(video,lock)


if __name__ == '__main__':
    main()
