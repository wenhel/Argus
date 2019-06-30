#!/bin/bash

env_dir="python_env"
path=`pwd`
path_to_env_dir="$path/$env_dir"

if [ -d $path_to_env_dir ];then
  . ./$env_dir/bin/activate
else
  virtualenv -p /usr/bin/python2 $env_dir
  . ./$env_dir/bin/activate
  python -m pip --no-cache-dir install -r requirements.txt
fi
