#!/usr/bin/env python
#-*- coding: utf-8 -*-

import urllib

def download_graph(url, path):
    # proxies = {'http': 'http://10.0.1.77:443'}
    response = urllib.urlopen(url)
    con = response.read()
    output_file = open(path,'wb')
    output_file.write(con)
    output_file.close()

if __name__ == '__main__':
    pic_url = 'https://i.imgur.com/fFPslSH.jpg'
    download_graph(pic_url, '1.jpg')
