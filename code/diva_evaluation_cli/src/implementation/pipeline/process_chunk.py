import argparse
import diva_pipeline_v2 as diva_pipeline
import sys


def cmd_arguments():
  parser = argparse.ArgumentParser(description='''
  functions: operate CMU DIVA pipeline.
  ''', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--chunk_id',dest='chunk_id', type=str,  help='''
  the chunk_id
  ''')
  parser.add_argument('--out_file',dest='out_file', type=str,  default=None, help='''
  the out_file
  ''')
  parser.register('type', 'bool', str2bool)
  parser.add_argument('--test', dest='test', type='bool', default=False, help='''enable for testing''')
  args = parser.parse_args()
  return args


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    if v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def do_job(args):
  diva_pipeline.main(args.chunk_id, args.out_file)

def main():
  args = cmd_arguments()
  do_job(args)
  sys.exit()

if __name__ == '__main__':
  main()