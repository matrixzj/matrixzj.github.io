#! /bin/bash

tmpDir='/tmp/keycaps'
profile='SA'

sed -ne "/## ${profile}/{:a;N;/GMK/!ba;p}" index.md > ${tmpDir}/${profile}

for year in $(seq 2013 2019); do 
    last2DigitYear=${year:0-2}
    previousYear=$(expr ${year} - 1)
    
    grep "### ${previousYear}" ${tmpDir}/${profile} > /dev/null 
    
    if [ $? -ne 0 ]; then
        previousYear='---'
    fi
    
    sed -ne "/### ${year}/{:a;N;/${previousYear}/!ba;p}" ${tmpDir}/${profile} | grep '^\*' > ${tmpDir}/${profile}-${year}
    
    order=5
    while read -r line; do 
        fileName=$(echo "${line}" | awk -F'(' "{print \$2}" | awk -F')' "{print \$1}" | sed -e "s/\(.*\)\//\1.md/")
        fileOrder=$(echo "(50-${last2DigitYear})*1000+${order}" | bc)
        order=$(expr ${order} + 5)
        sed -i "/nav_order/s/.*/nav_order: ${fileOrder}/" ${fileName}
    done < ${tmpDir}/${profile}-${year}
done
