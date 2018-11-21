#! /usr/bin/python

from sys import argv
from os import listdir
from os.path import isfile, join

script, filepath = argv

name = 'Penumbra'
keycapstype = 'SA'
rate = 6.07
designer = 'Bunny'
profile = '%s 1-2-3-3-4-4' % ( keycapstype.upper() )
colorcodes = ''

print "---\ntitle: %s\nlayout: default\nicon: fa-keyboard-o\nparent: %s Keycaps\nnav_order: 1\n---\n\n# %s\n\nref link: []()\n\n* [Price](#price)\n* [Kits](#kits)\n* [Info](#info)\n* [Pictures](#pictures)\n\n## Price" % (name, keycapstype, name)

print 'NOTE: USD to RMB exchange rate is %.2f' % (float(rate))

# generate price table
print """
| Name          | Price(USD)    |  Price(RMB) |  Price(ZF) | Quantity |
| ------------- | ------------- |  ---------- |  --------- | -------- |"""
with open(filepath) as fp:  
   line = fp.readline()
   cnt = 1
   while line:
       kitname = line.split('|')[0]
       usdprice = line.split('|')[1]
       rmbprice = line.split('|')[2]
       zfprice = line.split('|')[3]
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

       if len(zfprice) > 1:
          result_zfprice = '%.2f|' % float(zfprice)
       else: 
          result_zfprice = 'unknown|'
       result = result + result_zfprice

       if len(quantity) > 1:
          result_quantity = '%d|' % (int(quantity))
       else: 
          result_quantity = 'unknown|'
       result = result + result_quantity

       print result

       line = fp.readline()
       cnt += 1

print ''
print '<img src="{{ \'assets/images/%s-keycaps/%s/price.jpg\' | relative_url }}" alt="price" class="image featured">' % (keycapstype, name.lower().replace(" ",""))
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
       zfprice = line.split('|')[3]
       quantity = line.split('|')[-1]

       if len(usdprice) < 1:
          usdprice = 'unknown'
          result = '**Price(USD):** %s    ' % (usdprice)
       else:
          usdprice = float(usdprice)
          result = '**Price(USD):** %.2f    ' % usdprice

       if type(usdprice) is float:
          rmbprice = float(usdprice) * float(rate)
          result = result + '**Price(RMB):** %.2f    ' % (float(rmbprice))
       elif len(rmbprice) > 1:
          rmbprice = float(rmbprice)
          result = result + '**Price(RMB):** %.2f    ' % (float(rmbprice))
       else:
          rmbprice = 'unknown'
          result = result + '**Price(RMB):** ' + rmbprice
          
       
       if len(zfprice) > 1:
          result_zfprice = '    **Price(ZF):** %.2f    ' % (float(zfprice))
       else: 
          result_zfprice = '    **Price(ZF):** unkown'
       result = result + result_zfprice

       if len(quantity) > 1:
          result_quantity = '    **Quantity:** %d' % (int(quantity))
       else: 
          result_quantity = '    **Quantity:** unknown'
       result = result + result_quantity

       print "### %s" % kitname
       print result
       print '<img src="{{ \'assets/images/%s-keycaps/%s/kits_pics/%s.jpg\' | relative_url }}" alt="%s" class="image featured">' % ( keycapstype, name.lower().replace(" ",""), kitname.lower().replace(" ",""), kitname.replace(" ","") )
       print ''
       line = fp.readline()
       cnt += 1

# generate info part
print """## Info
* Designer: %s
* Profile: %s""" % (designer, profile)
print "* Color Codes: %s  " % (colorcodes)
for color in colorcodes.split('/'):
    print '<img src="{{ \'assets/images/SP_ColorCodes/abs/SP_Abs_ColorCodes_%s.png\' | relative_url }}" alt="color%s" height="150" width="340">' % (color, color)

# generate picture part
print """
## Pictures"""
picpath = '/home/juzou/documents/matrixzj.github.io/assets/images/%s-keycaps/%s/rendering_pics/' % (keycapstype.lower(), name.lower().replace(" ",""))
pictures = [f for f in listdir(picpath)]
for pic in pictures:
   print '<img src="{{ \'assets/images/%s-keycaps/%s/rendering_pics/%s\' | relative_url }}" alt="%s" class="image featured">' % ( keycapstype, name.lower().replace(" ",""), pic, pic.replace(".jpg","") )
