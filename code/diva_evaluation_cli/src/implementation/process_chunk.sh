#!/bin/bash

CHUNK_ID=$1
OUT_FILE=$2
# nvidia-docker exec rc3d /bin/bash \
# -c "python /diva/R-C3D/experiments/virat/main_wrapper.py \
# --exp /diva/R-C3D/experiments/virat/experiment.yml --skip_train --chunk_id=${CHUNK_ID}"

cd "$(dirname "$0")"
if [ -z $OUT_FILE ];then
	python pipeline/process_chunk.py --chunk_id ${CHUNK_ID}
else
	python pipeline/process_chunk.py --chunk_id ${CHUNK_ID} --out_file=$OUT_FILE
fi