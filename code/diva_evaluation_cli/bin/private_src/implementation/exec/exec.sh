#!/bin/bash

cd "$(dirname "$0")"

file_index=$1
activity_index=$2
chunks=$3
number_of_videos=$4
video_location=$5
system_cache_dir=$6
config=$7
output=$8
chunks_result=$9

tmp_file="chunk_ids.tmp"

function should_exit {
  exit_status=$1
  if [ $exit_status -ne 0  ];then
    exit 1
  fi
}

function should_cleanup_exit {
  exit_status=$1
  if [ $exit_status -ne 0  ];then
    actev experiment-cleanup
    exit 1
  fi
}

function should_continue {
  exit_status=$1
  chunk_id=$2
  system_cache_dir=$3
  if [ $exit_status -ne 0  ];then
    actev reset-chunk -i $chunk_id -s $system_cache_dir
    if [ $? -ne 0 ];then
      exit 1
    else
      continue
    fi
  fi
}

actev design-chunks -f $file_index -a $activity_index -o $chunks -n $number_of_videos
should_exit $?
actev experiment-init -f $file_index -a $activity_index -c $chunks -v $video_location -s $system_cache_dir -C $config
should_cleanup_exit $?

# Get chunks
python3 get_chunks_ids.py $chunks $tmp_file
should_cleanup_exit $?

for chunk_id in $(cat $tmp_file); do
  actev pre-process-chunk -i $chunk_id -s $system_cache_dir
  should_continue $? $chunk_id $system_cache_dir
  actev process-chunk -i $chunk_id -s $system_cache_dir 
  should_continue $? $chunk_id $system_cache_dir
  actev post-process-chunk -i $chunk_id -s $system_cache_dir 
  should_continue $? $chunk_id $system_cache_dir
done
rm $tmp_file

actev merge-chunks -o $output -c $chunks_result -r $system_cache_dir
actev experiment-cleanup
