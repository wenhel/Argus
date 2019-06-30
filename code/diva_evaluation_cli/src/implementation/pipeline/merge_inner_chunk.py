# call_inner_merge.py
import shlex
import os
from DivaLogger import DivaLogger
from subprocess import Popen, PIPE, STDOUT, CalledProcessError
CURRENT_PATH = os.path.split(os.path.realpath(__file__))[0]

def _call_shell_logging(cmd):
        '''
        cmd to pipe
        '''
        if not isinstance(cmd, list):
            print('warn: callshell_logging:Exception: cmd must be a list')
            return False
        try:
            process = Popen(
                ' '.join(cmd),
                stdout=PIPE,
                stderr=STDOUT,
                shell=True,
                universal_newlines=True,
                bufsize=20)
            while True:
                line = process.stdout.readline().decode()
                if not line:
                    break
            returncode = process.wait()
        except CalledProcessError as exception:
            print('error: callshell_logging:Exception occured: ' +
                         str(exception))
            print('error: callshell_logging failed')
            return False
        else:
            print('warn: callshell: finished')
        return (returncode == 0)


def inner_merge(video_lst_file,actev_conv_rnn_dir,p1b_conv_rnn_dir,out_file):
	cmd = ['python', os.path.join(CURRENT_PATH, 'merge.py'),
			'--video_lst_file',video_lst_file,
			'--actev_conv_rnn_dir',actev_conv_rnn_dir,
			'--p1b_conv_rnn_dir',p1b_conv_rnn_dir,
			'--out_file',out_file,
			]
	success = _call_shell_logging(cmd)

	return success
