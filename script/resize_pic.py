#! /usr/bin/python

import PIL
from PIL import Image
from sys import argv
import os

script, sourceFilePath, sourceFileName = argv

sourceFile = sourceFilePath + '/' + sourceFileName
img = Image.open(sourceFile)
finalw = img.size[0] * 0.7
finalh = img.size[1] * 0.7

img = img.resize((int(finalw), int(finalh)), PIL.Image.ANTIALIAS)

targetFileName = sourceFilePath + '/resized_' + sourceFileName
img.save(targetFileName)
