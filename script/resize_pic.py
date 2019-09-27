#! /usr/bin/python

import PIL
from PIL import Image
from sys import argv
import sys
import os

script, sourceFilePath, sourceFileName = argv

sourceFile = sourceFilePath + '/' + sourceFileName
img = Image.open(sourceFile)
if img.mode == "RGBA": 
    rgb_img = img.convert('RGB')
    targetRGBFile = sourceFilePath + '/rgb_' + sourceFileName
    rgb_img.save(targetRGBFile)
    os.rename(targetRGBFile, sourceFile)
    sys.exit(0)

finalw = img.size[0] * 0.7
finalh = img.size[1] * 0.7

img = img.resize((int(finalw), int(finalh)), PIL.Image.ANTIALIAS)

targetFileName = sourceFilePath + '/resized_' + sourceFileName
img.save(targetFileName)
os.rename(targetFileName, sourceFile)
