#!/bin/bash

url=$1
location=$2
user=$3
password=$4
token=$5

if [ $location != "None" ];then
  cd $location
fi

if [ $token != "None" ]; then
  curl "Authorization: Bearer $token" $url
else
  if [ $user != "None" ] && [ $password != "None" ];then 
    curl -u $user:$password $url
  else
    if [ $user != "None" ] && [ $password == "None" ];then
      curl -u $user $url
    else
      curl $url
    fi
  fi
fi

