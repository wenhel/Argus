#!/bin/bash

url=$1
location=$2
user=$3
password=$4
token=$5
cli=$6

# If there are credentials
if [ $user != "None" ];then
  if [ $password != "None" ]; then
    credentials="${user}:${password}@"
  else
    if [ $token != "None" ];then
      credentials="${user}:${token}@"
    else
      credentials=""
    fi
  fi

  http=`echo $url | cut -d '/' -f1`
  git=`echo $url | cut -d '/' -f3`
  end=`echo $url | cut -d '/' -f4-`
  url="${http}//${credentials}${git}/${end}"
fi

# If there is a location
if [ $location != "None" ];then
  cd $location
fi

git clone $url

if [ $? -eq 0 ];then
  # If the system has to be installed
  if [ $cli == "True" ];then
    repo_name=`echo $url | rev | cut -d '.' -f2 | rev`
    repo_name=`echo $repo_name | rev | cut -d '/' -f1 | rev`
    cd $repo_name

    diva_evaluation_cli/bin/install.sh
  fi
fi
