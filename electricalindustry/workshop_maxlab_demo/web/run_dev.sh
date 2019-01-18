#!/usr/bin/env bash

os_name=$(uname)
if [[ "$os_name" == 'Linux' ]]; then
   get_path=readlink
elif [[ "$os_name" == 'Darwin' ]]; then
   get_path=greadlink
fi

work_dir=$(dirname $($get_path -f $0))
cd $work_dir

npm install
./node_modules/quasar-cli/bin/quasar dev
