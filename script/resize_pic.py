#! /usr/bin/python

import PIL
from PIL import Image
from sys import argv

script, sourceFileName = argv

img = Image.open(sourceFileName)
finalw = img.size[0] * 0.7
finalh = img.size[1] * 0.7

img = img.resize((int(finalw), int(finalh)), PIL.Image.ANTIALIAS)

targetFileName = 'resized_' + sourceFileName
img.save(targetFileName)
