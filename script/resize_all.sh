#! /bin/bash 

path=$1

for i in $(find $path -size +300k -print); do
    fileName=$(echo $i | awk -F'/' '{print $NF}')
    echo $fileName
    /home/juzou/documents/matrixzj.github.io/script/resize_pic.py $fileName
    mv -f "resized_$fileName" "$fileName"
done
