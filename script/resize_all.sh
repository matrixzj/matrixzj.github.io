#! /bin/bash 

path=$1

# resize rendering pictures
for i in $(find rendering_pics/$path -size +400k -print); do
    fileName=$(echo $i | awk -F'/' '{print $NF}')
    echo $fileName
    /home/jzou/keyboard/web/script/resize_pic.py rendering_pics $fileName
    mv -f "rendering_pics/resized_$fileName" "rendering_pics/$fileName"
done

# resize kits pictures
for i in $(find kits_pics/$path -size +300k -print); do
    fileName=$(echo $i | awk -F'/' '{print $NF}')
    echo $fileName
    /home/jzou/keyboard/web/script/resize_pic.py kits_pics $fileName
    mv -f "kits_pics/resized_$fileName" "kits_pics/$fileName"
done
