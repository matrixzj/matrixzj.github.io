#! /bin/bash

url=$1

name=$(echo ${url} | awk -F'/' '{print $NF}')

wget $url -O ${name}.html

# egrep 'jpg|png|psd' ${name}.html | grep ${name} > ${name}.html.pic
egrep 'jpg|png|psd' ${name}.html > ${name}.html.pic
sed -i 's/jpg/jpg\n/g' ${name}.html.pic
sed -i 's/png/png\n/g' ${name}.html.pic
sed -i 's/psd/psd\n/g' ${name}.html.pic
sed -i 's/.*\(https.*jpg\).*/\1/' ${name}.html.pic
sed -i 's/.*\(https.*png\).*/\1/' ${name}.html.pic
sed -i 's/.*\(https.*psd\).*/\1/' ${name}.html.pic

#for pic in $(grep '^https' ${name}.html.pic | grep ${name} | sort -u); do 
for pic in $(grep '^https' ${name}.html.pic | sort -u); do 
	pic_name=$(echo ${pic} | awk -F'/' '{print $NF}')
	wget $pic -O ${pic_name}
done

