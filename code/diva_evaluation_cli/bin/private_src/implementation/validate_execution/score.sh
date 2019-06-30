#!/bin/bash

cd "$(dirname "$0")"

# Get the ActEV scorer submodule
git submodule update --init --recursive
if [ $? -ne 0 ];then
  exit 1
fi

# Configure the scorer with the right arguments
output=$1
reference=$2
activity=$3
file=$4
result=$5

# Execute ActEV Scorer
cd ActEV_Scorer

python2 ActEV_Scorer.py \
	ActEV18_AD \
	-s $output \
	-r $reference \
	-a $activity \
	-f $file \
	-o $result \
	-v 
