#!/bin/bash
cd "$(dirname "$0")"

chunk_id=$1
system_cache_dir=$2

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

echo "Pre-processing ${1}..."
python pipeline/pre_process_chunk.py $chunk_id
echo "${1} pre-processed"
should_exit $?
