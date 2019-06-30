import argparse
import os
import json
import traceback


def cmd_arguments():
  parser = argparse.ArgumentParser(description='''
functions:
merge output from different models in one chunk
    ''', 
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('--video_lst_file', dest='video_lst_file', help='''
the path of video list, in this file each line is the relative path of the video to the video_dir. 
That is, video_file_path = os.path.join(video_dir, ${line})
    ''')

  parser.add_argument('--actev_conv_rnn_dir', dest='actev_conv_rnn_dir', help='''
actev_conv_rnn model output directory
    ''')

  parser.add_argument('--p1b_conv_rnn_dir', dest='p1b_conv_rnn_dir', help='''
p1b_conv_rnn model output directory
    ''')

  parser.add_argument('--out_file', dest='out_file', type=str, help='''
out_file full path
    ''')

  args = parser.parse_args()

  return args


def do_job(args):
  file_processed = []
  activitys = []

  names = []
  videos = []
  with open(args.video_lst_file) as f:
    for line in f:
      line = line.strip()
      videos.append(line)
      name, _ = os.path.splitext(line)
      names.append(name)

  for name, video in zip(names, videos):
    print 'processing...', name
    actev_conv_rnn_file = os.path.join(args.actev_conv_rnn_dir, name + '.json')
    p1b_conv_rnn_file = os.path.join(args.p1b_conv_rnn_dir, name + '.json')


    print 'actev_conv_rnn'
    if os.path.exists(actev_conv_rnn_file):
      with open(actev_conv_rnn_file) as f:
        data = json.load(f)
      video = data['filesProcessed'][0]
      for activity in data['activities']:
          if activity['activity'] == 'Riding':
            objects = activity['objects']
          failed = False
          for obj in objects:
            localization = obj['localization']
            if len(localization.values()[0]) < 2:
              failed = True
              break

          if not failed:
            activity['activityID'] = len(activitys)
            activitys.append(activity)

    print 'p1b_conv_rnn'
    if os.path.exists(p1b_conv_rnn_file):
      with open(p1b_conv_rnn_file) as f:
        data = json.load(f)
      for activity in data['activities']:
          if activity['activity'] == 'Riding' or activity['activity'] == 'Interacts': ## CLASS Interacts is removed
            continue
          objects = activity['objects']
          failed = False
          for obj in objects:
            localization = obj['localization']
            if len(localization.values()[0]) < 2:
              failed = True
              break

          if not failed:
            activity['activityID'] = len(activitys)
            activitys.append(activity)

    file_processed.append(video)

  out = {
    'filesProcessed': file_processed,
    'activities': activitys,
  }
  with open(args.out_file, 'w') as fout:
    json.dump(out, fout, indent=2)


def main():
  args = cmd_arguments()
  try:
    do_job(args)
  except:
    traceback.print_exc()


if __name__ == '__main__':
  main()
