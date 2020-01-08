#!/bin/bash

file=$1
histroy_graph=$2 
order_graph=$3

# get download location
download_dest=$(grep 'image.*kit' ${file} | head -n 1 | sed -e "s/.*{{ '\(.*\)'.*/\1/" | awk -F'/' 'BEGIN{OFS="/"}{print $1,$2,$3,$4}')

# download history graph
suffix=$(echo ${histroy_graph} | awk -F'.' '{print $NF}')
wget -e use_proxy=yes -e http_proxy=10.0.1.77:443 ${histroy_graph} -O ${download_dest}/history.${suffix}

# download order graph
suffix=$(echo ${order_graph} | awk -F'.' '{print $NF}')
wget -e use_proxy=yes -e http_proxy=10.0.1.77:443 ${order_graph} -O ${download_dest}/order.${suffix}

# check graph info is there or not
grep '## Kits' -B2 ${file} | grep histrory > /dev/null

if [ $? -ne 0 ]; then
    sed -i "/## Kits/i\<img src=\"{{ '${download_dest}/history.${suffix}' | relative_url }}\" alt=\"history\" class=\"image featured\">" ${file}
fi

# check  info is there or not
grep '## Kits' -B2 ${file} | grep order > /dev/null

if [ $? -ne 0 ]; then
    sed -i "/## Kits/i\<img src=\"{{ '${download_dest}/order.${suffix}' | relative_url }}\" alt=\"order\" class=\"image featured\">\n" ${file}
fi
