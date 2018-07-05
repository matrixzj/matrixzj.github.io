#! /usr/bin/python

from PIL import Image
from resizeimage import resizeimage
from sys import argv
import os

script, filename = argv
dstfilename = filename + ".png"

im = Image.open(filename)
im.resize((340, 150)).save(dstfilename)
os.rename(dstfilename, filename)
