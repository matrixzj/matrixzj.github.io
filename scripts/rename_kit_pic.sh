#! /bin/bash

file=$1

awk -F'|' '{print $1}' ${file} > ${file}.name

ls -al images/kits_pics | tail -n +4 | awk '{print NR,$NF}'> kits.list
awk '{gsub(/_/,""); print NR,$NF}' kits.list > kits.list1
join kits.list kits.list1 | awk '{printf("%s|%s\n",$2,$3)}' > kits.list.final

while read -r line; do
	count=$(grep -i "$line" kits.list.final | wc -l)
	if [ $count -eq 1 ]; then 
		srcfilename=$(grep -i "$line" kits.list.final | awk -F'|' '{print $1}')
		echo $srcfilename
	 	dstfilename=$(echo $line | sed -e 's/.*/\L&.jpg/')	
		echo $dstfilename
		mv images/kits_pics/$srcfilename images/kits_pics/$dstfilename
#	if [ $count -gt 1 ]; then 
		echo $line
	fi
done < ${file}.name
 


