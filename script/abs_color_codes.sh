#! /bin/bash

for i in $(sed -ne 's/.*SP_Abs_ColorCodes_\(.*\).png/\1/p' /tmp/orange_list); do 
    colorCode=$i; 
    colorSample=$(egrep -B2 "\s$i\s" /tmp/sp.html | sed -ne '/td/{N;s/\n//;p}' | sed -e 's/td/th/g')
    RGBCode=$(egrep -A5 "\s$i\s" /tmp/sp.html | sed -ne '/td/{N;s/\n//;p}' | sed -ne '/RGB/p' | sed -e 's/td/th/g' | sed -e 's/<th>RGB(\(.*\))/<th>\1/')
    HEXCode=$(egrep -A5 "\s$i\s" /tmp/sp.html | sed -ne '/td/{N;s/\n//;p}' | sed -ne '/tr/s/<\/tr>//p' | sed -e 's/td/th/g' | sed -e 's/<th>(\(.*\))/<th>\1/')

    printf "  <tr>\n"
    printf "    %s\n" "$colorSample"
    printf "    <th><b> %s </b></th>\n" "$colorCode"
    printf "    %s\n" "$RGBCode"
    printf "    %s\n" "$HEXCode"
    printf "    <th><img src=\"{{ 'assets/images/sa-keycaps/SP_ColorCodes/abs/SP_Abs_ColorCodes_%s.png' | relative_url }}\" alt=\"color%s\" height=\"75\" width=\"170\"></th>\n" "$colorCode" "$colorCode"
    printf "  </tr>\n"
#    echo $RGBCode
#    echo $HEXCode
done
