#!/bin/bash

#####################################################
# Command Line Interface actev: installation script #
#####################################################

CURRENT_DIR=`pwd`
cd "$(dirname "$0")"

# Determine if python is running in a virtual environment
python3 private_src/implementation/utils/is_virtual_env.py
EXIT_STATUS=$?

cd "${CURRENT_DIR}"
if [ $EXIT_STATUS -ne 0 ];then

  # Check that .local/bin path is in $PATH
  echo $PATH | grep /.local/bin > /dev/null
  EXIT_STATUS=$?

  if [ $EXIT_STATUS -ne 0 ];then
    echo "Please add ~/.local/bin to your PATH  before running the script:"
    echo "export PATH=\"${PATH}:${HOME}/.local/bin\""
    exit 1
  fi

  # Install using python3
  options='--user'
else
  # Install using venv python
  options=''
fi

cd "$(dirname "$0")"

sudo apt-get install python3-pip -y
sudo apt-get install python3-dev -y

python3 -m pip install setuptools $options
python3 -m pip install -r ../../requirements.txt $options
python3 -m pip install -e ../../. -U $options

