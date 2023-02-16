#! /bin/bash 

path=$1

for subpath in $(find ${path} -type d); do 
    for i in $(find ${subpath} -type f -maxdepth 1 -size +400k -print); do
        fileName=$(echo $i | awk -F'/' '{print $NF}')
        echo ${fileName}
        /home/jzou/keyboard/web/script/resize_pic.py ${subpath} ${fileName}
    done
done
