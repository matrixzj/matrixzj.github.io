#! /bin/bash 

path=$1

# resize rendering pictures
for i in $(find $path/rendering_pics/ -size +400k -print); do
    fileName=$(echo $i | awk -F'/' '{print $NF}')
    echo $fileName
    /home/jzou/keyboard/web/script/resize_pic.py $path/rendering_pics $fileName
done

# resize kits pictures
for i in $(find $path/kits_pics/ -size +400k -print); do
    fileName=$(echo $i | awk -F'/' '{print $NF}')
    echo $fileName
    /home/jzou/keyboard/web/script/resize_pic.py $path/kits_pics $fileName
done
