#! /usr/bin/python

from sys import argv
from os import listdir
from os.path import isfile, join

script, filepath = argv

name = 'Banana'
rate = 6.87
designer = 'FF'
profile = '1-1-2-3-4-4'
colorcodes = 'YBP/SCK/GX'

print """---
title: SA 
author: Matrix Zou
layout: post
icon: fa-keyboard-o
tags: [ keycaps ]
---

ref link: []()

* [Price](#price)
* [Kits](#kits)
* [Info](#info)
* [Pictures](#pictures)

## Price
"""
print 'NOTE: USD to RMB exchange rate is %.2f' % (float(rate))

# generate price table
print """
| Name          | Price(USD)    |  Price(RMB)  | Quantity |
| ------------- | ------------- |  ---------- | -------- |"""
with open(filepath) as fp:  
   line = fp.readline()
   cnt = 1
   while line:
       kitname = line.split('|')[0]
       usdprice = line.split('|')[1]
       rmbprice = line.split('|')[2]
#       kpprice = line.split('|')[3]
       quantity = line.split('|')[-1]

       result = '|[%s](#%s)|' % (kitname, kitname.lower().replace(" ",""))

       if len(usdprice) < 1:
          usdprice = 'unknown'
          result = result + usdprice + '|'
       else:
          usdprice = float(usdprice)
          result = ("%s%.2f|") % (result, usdprice)


       if type(usdprice) is float:
          rmbprice = float(usdprice) * float(rate)
          result = ("%s%.2f|") % (result, float(rmbprice))
       elif len(rmbprice) > 1:
          rmbprice = float(rmbprice)
          result = ("%s%.2f|") % (result, float(rmbprice))
       else:
          rmbprice = 'unknown|'
          result = result + rmbprice

#       if len(kpprice) > 1:
#          result_kpprice = '%.2f|' % (float(kpprice))
#       else: 
#          result_kpprice = 'unknown|'
#       result = result + result_kpprice

       if len(quantity) > 1:
          result_quantity = '%d|' % (int(quantity))
       else: 
          result_quantity = 'unknown|'
       result = result + result_quantity

       print result

       line = fp.readline()
       cnt += 1

print ''
print '<img src="{{ \'assets/images/%s/Price.jpg\' | relative_url }}" alt="price" class="image featured">' % name.lower().replace(" ","")
print ''

# generate kits part
print '## Kits'
with open(filepath) as fp:  
   line = fp.readline()
   cnt = 1
   while line:
       kitname = line.split('|')[0]
       usdprice = line.split('|')[1]
       rmbprice = line.split('|')[2]
#       kpprice = line.split('|')[3]
       quantity = line.split('|')[-1]

       if len(usdprice) < 1:
          usdprice = 'unknown'
          result = '**Price(USD):** %s \t' % (usdprice)
       else:
          usdprice = float(usdprice)
          result = '**Price(USD):** %.2f\t' % usdprice

       if type(usdprice) is float:
          rmbprice = float(usdprice) * float(rate)
          result = result + '**Price(RMB):** %.2f\t' % (float(rmbprice))
       elif len(rmbprice) > 1:
          rmbprice = float(rmbprice)
          result = result + '**Price(RMB):** %.2f\t' % (float(rmbprice))
       else:
          rmbprice = 'unknown'
          result = result + '**Price(RMB):** ' + rmbprice
          
       
#       if len(kpprice) > 1:
#          result_kpprice = '\t**Price(KP):** %.2f' % (float(kpprice))
#       else: 
#          result_kpprice = '\t**Price(KP):** unkown'
#       result = result + result_kpprice

       if len(quantity) > 1:
          result_quantity = '\t**Quantity:** %d' % (int(quantity))
       else: 
          result_quantity = '\t**Quantity:** unknown'
       result = result + result_quantity

       print "#### %s" % kitname
       print result
       print '<img src="{{ \'assets/images/%s/kits_pics/%s.jpg\' | relative_url }}" alt="%s" class="image featured">' % ( name.lower().replace(" ",""), kitname.lower().replace(" ",""), kitname.replace(" ","") )
       print ''
       line = fp.readline()
       cnt += 1

# generate info part
print """## Info
* Designer: %s
* Profile: SA %s""" % (designer, profile)
print "* Color Codes: %s  " % (colorcodes)
for color in colorcodes.split('/'):
    print '<img src="{{ \'assets/images/SP_ColorCodes/abs/SP_Abs_ColorCodes_%s.png\' | relative_url }}" alt="color%s" height="150" width="340">' % (color, color)

# generate picture part
print """
## Pictures"""
picpath = '../assets/images/%s/rendering_pics/' % name.lower().replace(" ","")
pictures = [f for f in listdir(picpath)]
for pic in pictures:
   print '<img src="{{ \'assets/images/%s/rendering_pics/%s\' | relative_url }}" alt="%s" class="image featured">' % ( name.lower().replace(" ",""), pic, pic.replace(".jpg","") )
