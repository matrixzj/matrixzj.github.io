#!/bin/bash

grep SP_Color $1 | grep '^<img' > /tmp/test

sed -i '/* Color Codes/s/\(* Color Codes:\).*/\1  /' $1
sed -i '/^<img.*SP_Color.*/d' $1

cat > /tmp/test_color << EOF
<table style="width:100%">
  <tr>
    <th>ColorCodes</th>
    <th>Sample</th>
  </tr>
EOF

while read -r line; do color_codes=$(echo $line | awk '{print $7}' | sed -ne 's/.*color\(.*\)"/\1/p'); printf "  <tr>\n    <th>%s</th>\n    <th>%s</th>\n  </tr>\n" $color_codes "${line}"; done < /tmp/test >> /tmp/test_color

echo "</table>" >> /tmp/test_color

sed -i 's/150/75/' /tmp/test_color
sed -i 's/340/170/' /tmp/test_color

sed -i '/* Color Codes/r /tmp/test_color' $1

rm -f /tmp/test
rm -f /tmp/test_color
