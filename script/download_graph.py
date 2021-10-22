#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
import magic
import os
import sys
import re

TEMP_PIC_FILE = '/tmp/KEYCAP_PIC_FILE'

def download_graph(url, path, sub_path, name):

    pattern = r"%s\..*" % name
    for file_name in os.listdir(os.path.join(path, sub_path)):
        if re.match(pattern, file_name):
            file_path_name = os.path.join(path, sub_path, file_name)
            return file_path_name

    # proxies = {'http': 'http://10.0.1.77:443'}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers, verify=False)
    output_file = open(TEMP_PIC_FILE,'wb')
    output_file.write(response.content)
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
    print(sys.argv[1])
    pic_url = sys.argv[1]
#    download_graph(pic_url, '/tmp', '', 'imagetemp')
    KEYCAP_ASSETS_WITH_PATH = 'assets/images/gmk-keycaps/Sixes'
    sub_path='kits_pics'
    name = 'base'
    download_graph(pic_url, KEYCAP_ASSETS_WITH_PATH, sub_path, name)
