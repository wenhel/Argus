#!/bin/bash

# nvidia-docker stop rc3d
# sleep 1
# nvidia-docker rm rc3d
cd "$(dirname "$0")"
filename=$PWD/pipeline/config/module.lst
# dockerdir=/mnt/docker_images ## cache_dir
# prefix='https://s3.us-east-2.amazonaws.com/cmu-actev/docker_images'
# aws s3 cp dockers s3://cmu-actev/main/dockers --recursive
# docker rmi -f $(docker images|grep actev|awk '{print $3}')
# sudo mkdir -p $dockerdir
# cd $dockerdir
echo clearning previous containers...
for name in $(cat $filename|awk -F ":" '{print $1}'); do
	containers=$(docker ps -a|grep $name|awk '{print $1}'|uniq)
	if [   ! -z "$containers"  ]; then
		for cid in $containers;do
			nvidia-docker stop $cid 1>/dev/null 2>/dev/null
			sleep 2
			nvidia-docker rm $cid 1>/dev/null 2>/dev/null
		done
	fi
done
echo clearning previous containers... done.
echo NOTICE: We donot clean the chunk-wise result directory. If you want to do that, use actev reset-chunk -i  CHUNK_ID -s SYSTEM_CACHE_DIR