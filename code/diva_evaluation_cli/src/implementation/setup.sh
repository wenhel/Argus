#!/bin/bash

SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
prefix='https://s3.us-east-2.amazonaws.com/cmu-actev/docker_images'
filename=$SHELL_FOLDER/pipeline/config/module.lst
dockerdir=/tmp/actev_docker_images/
mkdir -p $dockerdir

FLAG_CLEAN_TAR=1 ## clean cached docker-image.tar

## configure docker images
cd $dockerdir
for name in $(cat $filename|awk -F ":" '{print $1}'); do
	names=$(docker images|grep $name|awk '{print $3}')
	if [ -n "$names" ]; then
		echo clearning docker image ${name}
		docker rmi -f $names
	fi 

	echo wgetting ${prefix}'/'${name}'.tar'
	 wget ${prefix}'/'${name}'.tar' -O $dockerdir/${name}'.tar'

	echo loading docker_images/${name}'.tar'
	docker load -i $dockerdir/${name}'.tar'

	if [ $FLAG_CLEAN_TAR -eq 1 -a -f $dockerdir/${name}'.tar' ]; then
		echo cleaning $dockerdir/${name}'.tar'
		 rm -rf $dockerdir/${name}'.tar'
	fi
	echo 'done:'${name}
done

