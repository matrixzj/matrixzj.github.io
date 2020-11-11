#! /usr/bin/python

import PIL
from PIL import Image
from sys import argv
import sys
import os

def resize_file(source_file):
    print(source_file)
    source_filename = source_file.split('/')[-1]
    img = Image.open(source_file)
    if img.mode == "RGBA":
        rgb_img = img.convert('RGB')
        target_RGB_file = '/tmp/tmp_rgb_' + source_filename
        rgb_img.save(target_RGB_file)
        os.rename(target_RGB_file, source_file)

    while os.stat(source_file).st_size > 409600:
        finalw = img.size[0] * 0.9
        finalh = img.size[1] * 0.9

        img = img.resize((int(finalw), int(finalh)), PIL.Image.ANTIALIAS)

        target_file = '/tmp/tmp_rgb_' + source_filename
        img.save(target_file) 
	os.rename(target_file, source_file)

if __name__ == '__main__':
    orig_size = os.stat(argv[1]).st_size
    resize_file(argv[1])
    final_size = os.stat(argv[1]).st_size
    print('orig_size: {}, final_size: {}'.format(orig_size, final_size))
