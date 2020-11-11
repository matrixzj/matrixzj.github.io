#!/usr/bin/env python
#-*- coding: utf-8 -*-

import urllib
import magic
import os

TEMP_PIC_FILE = '/tmp/KEYCAP_PIC_FILE'

def download_graph(url, path, sub_path, name):
    # proxies = {'http': 'http://10.0.1.77:443'}
    response = urllib.urlopen(url)
    con = response.read()
    output_file = open(TEMP_PIC_FILE,'wb')
    output_file.write(con)
    output_file.close()

    file_format = magic.from_file(TEMP_PIC_FILE, mime=True)

    if file_format == 'image/jpeg':
        file_ext = 'jpg'
        file_path_name = '{}.{}'.format(os.path.join(path, sub_path, str(name)), file_ext)
        os.rename(TEMP_PIC_FILE, file_path_name)
        return file_path_name
    elif file_format == 'image/png':
        file_ext = 'png'
        file_path_name = '{}.{}'.format(os.path.join(path, sub_path, str(name)), file_ext)
        os.rename(TEMP_PIC_FILE, file_path_name)
        return file_path_name
    else:
        print(file_format)
        return False

if __name__ == '__main__':
    pic_url = 'https://geekhack.org/index.php?action=dlattach;topic=109452.0;attach=255452;image'
    download_graph(pic_url, '/tmp/imagetemp')
