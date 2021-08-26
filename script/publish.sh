#! /bin/bash

echo "matrixzj.github.io"
~/config2git.sh ~/keyboard/web

echo "enjoykeycap.github.io"
sed -i '/Host github.com/,$s/^#\(\s*IdentityFile.*enjoykeycap\)/\1/;/Host github.com/,$s/\(^\s*IdentityFile.*id_rsa$\)/#\1/' ~/.ssh/config
~/config2git.sh ~/keyboard/enjoykeycap-github
sed -i '/Host github.com/,$s/^#\(\s*IdentityFile.*id_rsa\)/\1/;/Host github.com/,$s/\(^\s*IdentityFile.*enjoykeycap$\)/#\1/' ~/.ssh/config
