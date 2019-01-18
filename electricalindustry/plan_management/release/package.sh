#!/usr/bin/env bash

version='0.0.1'

os_name=$(uname)
if [[ "$os_name" == 'Linux' ]]; then
   get_path=readlink
elif [[ "$os_name" == 'Darwin' ]]; then
   get_path=greadlink
fi

work_dir=$(dirname $(dirname $($get_path -f $0)))
[ -d "${work_dir}/server/src/__pycache__" ] && rm -rf "${work_dir}/server/src/__pycache__"

for file in ${work_dir}/server/src/*
do [ -d $file ] && { app_name=${file##*/}; break; } done
echo "$app_name release version is $version"

cd $work_dir

package_dir="$work_dir/release/${app_name}_${version}"
mkdir $package_dir
cp -a ./server/bin ./server/lib ./server/src $package_dir
[ -d "${package_dir}/src/${app_name}/__pycache__" ] && rm -rf "${package_dir}/src/${app_name}/__pycache__"
rm -rf "${package_dir}/src/${app_name}/config.py"
mv "${package_dir}/src/${app_name}/config_product.py" "${package_dir}/src/${app_name}/config.py"

mkdir "${package_dir}/log"
mkdir "${package_dir}/static"

static_dir="../release/${app_name}_${version}/static"
cd "${work_dir}/web"

npm install
if [ $? -ne 0 ]; then
    echo "npm install error, packaging interrupt"
    exit -1
fi
./node_modules/quasar-cli/bin/quasar build
if [ $? -ne 0 ]; then
    echo "quasar build error, packaging interrupt"
    exit -1
fi

cp -a dist $static_dir

cd $package_dir
touch .already_package
touch .appid
echo '0-0-0-0-0' > .appid

cd "${work_dir}/release"
tar zvcf "${app_name}_${version}.tar.gz" "${app_name}_${version}"

cd $work_dir
rm -rf $package_dir

echo "finish"
