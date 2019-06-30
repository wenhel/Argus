#!/bin/bash

cd "$(dirname "$0")"
CHUNK_ID=$1
SYSTEM_CACHE_DIR=$2

echo "Reseting ${1}"
cd "$(dirname "$0")"
# OUTPUT=`echo "${CHUNK_ID}_sysfile.json"`
#rm -rf "${SYSTEM_CACHE_DIR}/${CHUNK_ID}"
rm pipeline/config/config_nist.yaml
