#!/usr/bin/env bash

venv_switch='on' # on/off

os_name=$(uname)
if [[ "$os_name" == 'Linux' ]]; then
   get_path=readlink
elif [[ "$os_name" == 'Darwin' ]]; then
   get_path=greadlink
fi

work_dir=$(dirname $(dirname $($get_path -f $0)))
for file in ${work_dir}/src/*
do [ -d $file ] && { app_name=${file##*/}; break; } done

cd $work_dir

major=$(python -c 'import sys; print(sys.version_info.major)')
minor=$(python -c 'import sys; print(sys.version_info.minor)')
if [[ $major -ne 3 || $minor -ne 6 ]]; then
    echo "python version error, python3.6 is required"
    exit -1
fi

if [ ! -f .already_package ]; then
    echo "can not install without packaging"
    exit -1
fi

if [[ "$venv_switch" == 'on' ]]; then
    [ -d env ] && rm -rf env
    virtualenv -p python env
    if [ $? -ne 0 ]; then
        echo "virtualenv error, installing interrupt"
        exit -1
    fi
    source env/bin/activate
fi

for item in $(ls lib/*.whl);do
    python -m pip install $item
    if [ $? -ne 0 ]; then
        echo "pip install error, installing interrupt"
        exit -1
    fi
done
for item in $(cat ./lib/requirements.txt);do
    python -m pip install $item
    if [ $? -ne 0 ]; then
        echo "pip install error, installing interrupt"
        exit -1
    fi
done

chmod u+x ./bin/run.sh
[ -f "/usr/local/sbin/${cmd_name}" ] && rm -f "/usr/local/sbin/${cmd_name}"
#cmd_name=run-${app_name/_/-}
#ln -s ${work_dir}/bin/run.sh  /usr/local/sbin/${cmd_name}


logstash_path="/etc/logstash/manugence/"

temp_logstash_conf_name=${work_dir//_/-}
logstash_conf_name=${temp_logstash_conf_name////_}

app_log_url=$work_dir"/log/*"
flag=False

if [[ ! -d $logstash_path ]]; then
    echo 'error: system missing logstash'
    flag=True
else
	for file in $logstash_path'*'
	do
	    if cat $file | grep "$app_log_url">/dev/null
        then
            echo 'info: app_log_url already configured'
            flag=True
            break
        fi
	done
fi

if [ $flag == False ]
then
    logstash_filename_path=${logstash_path}${logstash_conf_name}
    touch $logstash_filename_path

    echo 'input{
      file{
            path => "'${app_log_url}'"
            start_position => "beginning"
        }
    }' > $logstash_filename_path
fi

touch .already_install
echo 'info: finish'