#!/bin/bash

cd "$(dirname "$0")"
FILE_INDEX=$1
ACTIVITY_INDEX=$2
CHUNK=$3
VIDEO_LOCATION=$4
SYSTEM_CACHE_DIRECTORY=$5

## 1. cleaning containers
bash clean_up.sh
## 2. create nist.yaml 
python config_nist_yaml.py $FILE_INDEX $ACTIVITY_INDEX $CHUNK $VIDEO_LOCATION $SYSTEM_CACHE_DIRECTORY 



# TMP_FILE="videos.tmp"

# Clean the experiment if rc3d container already exists
# docker ps -a | grep rc3d 1> /dev/null
# if [ $? -eq 0  ];then
#   ./clean_up.sh
# fi



# FRAMES=`echo "${SYSTEM_CACHE_DIRECTORY}/frames"`

## 1.
# Transform videos into frames
## 1, the python script check the exist of frames of FILE_INDEX and if 
##  not it write the video name and frame path into TMP_FILE (a file)
## 2, the for loop extract frames of videos in the TMP_FILE 
## 3, after all it remove the tmp_file TMP_FILE

# python3 get_videos.py $FILE_INDEX $TMP_FILE $FRAMES
# for CONTENT in $(cat $TMP_FILE); do
#   VIDEO=`echo $CONTENT | cut -d ',' -f1`
#   FRAMES_PATH=`echo $CONTENT | cut -d ',' -f2`

#   mkdir -p "${FRAMES_PATH}"
#   ffmpeg -i "${VIDEO_LOCATION}/${VIDEO}" "${FRAMES_PATH}/%05d.png"
# done

# rm $TMP_FILE


## 2.
## we do this step at `proc-chunk`
# Start the rc3d container
# nvidia-docker run -itd --name rc3d \
#   -v ${FRAMES}:/data/diva/v1-frames \
#   -v ${SYSTEM_CACHE_DIRECTORY}:/data/diva/system-cache \
#   gitlab.kitware.com:4567/diva-baseline/diva-baseline:eval_cli 

# nvidia-docker exec rc3d mkdir -p /data/diva/nist-json
# nvidia-docker cp ${FILE_INDEX} rc3d:/data/diva/nist-json/file-index.json 
# nvidia-docker cp ${ACTIVITY_INDEX} rc3d:/data/diva/nist-json/activity-index.json 
# nvidia-docker cp ${CHUNK} rc3d:/data/diva/nist-json/chunk.json

