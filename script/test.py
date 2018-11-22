#! /usr/bin/python

from sys import argv
from os import listdir
from os.path import isfile, join

script, filepath = argv

f = open(filepath)
lineNumber = 1

# get Name
line = f.readline()
name = line.split("'")[1]
print name

