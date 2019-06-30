#!/bin/bash

url=$1
location=$2
user=$3
password=$4
token=$5

if [ $user != "None" ] && [ $password != "None" ];then 
  docker login --username $user --password $password
fi
docker pull $url
