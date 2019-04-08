#! /usr/bin/python

from sys import argv
from os import listdir
import os
from os.path import isfile, join

script, filepath = argv

rateDict = { "2019-01": '6.80', "2019-02": '6.79', "2019-03": '6.73',
    "2019-04": '6.73',
    "2018-12": '6.96', "2018-11": '6.95', "2018-10": '6.87', "2018-09": '6.95',
    "2018-08": '6.87', "2018-07": '6.67', "2018-06": '6.47', "2018-05": '6.42',
    "2018-04": '6.34', "2018-03": '6.28', "2018-02": '6.29', "2018-01": '6.29', 
    "2017-12": '6.53', "2017-11": '6.63', "2017-10": '6.65', "2017-09": '6.67',
    "2017-08": '6.61', "2017-07": '6.74', "2017-06": '6.80', "2017-05": '6.83',
    "2017-04": '6.91', "2017-03": '6.90', "2017-02": '6.88', "2017-01": '6.91',
    "2016-12": '6.97', "2016-11": '6.90', "2016-10": '6.79', "2016-09": '6.69',
    "2016-08": '', "2016-07": '', "2016-06": '', "2016-05": '',
    "2016-04": '', "2016-03": '', "2016-02": '', "2016-01": '',
    "2015-12": '', "2015-11": '', "2015-10": '', "2015-09": '',
    "2015-08": '', "2015-07": '', "2015-06": '', "2015-05": '',
    "2015-04": '', "2015-03": '', "2015-02": '', "2015-01": '',
    "2014-12": '', "2014-11": '', "2014-10": '', "2014-09": '',
    "2014-08": '', "2014-07": '', "2014-06": '', "2014-05": '',
    "2014-04": '', "2014-03": '', "2014-02": '', "2014-01": '',
    "2013-12": '', "2013-11": '6.10', "2013-10": '', "2013-09": '',
    "2013-08": '', "2013-07": '', "2013-06": '', "2013-05": '',
    "2013-04": '', "2013-03": '', "2013-02": '', "2013-01": '',
    "2012-12": '', "2012-11": '', "2012-10": '', "2012-09": '',
    "2012-08": '', "2012-07": '', "2012-06": '', "2012-05": '',
    "2012-04": '', "2012-03": '', "2012-02": '', "2012-01": '',}

lines = tuple(open(filepath, 'r'))

# get Name
name = lines[0].split("'")[1]

# get cName
cname = lines[1].split("'")[1]

# get keycaptype
keycapstype = lines[2].split("'")[1]

# get time
time = lines[5].split("'")[1]

# get rate
if rateDict[time]:
    rate = float(rateDict[time])
else:
    rate = ''

# get designer
designer = lines[3].split("'")[1]

# get profile
profile = lines[4].split("'")[1]

# get colorcodes
colorcodes = lines[6].split("'")[1]

# get plateform
platform = lines[7].split("'")[1]

# get link
link = lines[8].split("'")[1]

# generate navOrder
keycapPath = '/home/jzou/keyboard/web/docs/%s-keycaps/' % keycapstype.lower()
navOrder = ( len([eachfile for eachfile in os.listdir(keycapPath) if os.path.isfile(os.path.join(keycapPath, eachfile))]) - 1) * 5 + 10000

# key: name, usd, rmb, quantity
priceDict = {}
sn = 1
for line in lines[9:]:
    lengthLine = len(line.split("|"))
    if lengthLine == 5:
	hasQuantity = True
    else:
	hasQuantity = False 

    kitName = line.split("|")[0]

    kitUSD = line.split("|")[1]
    kitRMB = line.split("|")[2]
    if len(kitUSD) < 1 and len(kitRMB) < 1:
        kitUSD = 'unknown'
    elif len(kitUSD) < 1 and len(kitRMB) > 1:
        kitUSD = float(kitRMB) / rate
    else:
        kitUSD = float(kitUSD)

    print kitUSD
    print rate
    if len(kitRMB) < 1 and isinstance(kitUSD, float):
        kitRMB = float(kitUSD) * rate
    elif len(kitRMB) > 1:
        kitRMB = float(kitRMB)
    else:
    	kitRMB = 'unknown'

    if hasQuantity:
        kitQuantity = line.split("|")[3]
        
	if len(kitQuantity) < 1:
	    kitQuantity = 'unknown'
	else:
	    kitQuantity = int(kitQuantity)

    if hasQuantity:
	priceDict[sn] = [kitName, kitUSD, kitRMB, kitQuantity]
    else:
	priceDict[sn] = [kitName, kitUSD, kitRMB]
    sn += 1

if cname:
    print "---"
    print "title: %s %s" % (name, cname)
    print "layout: default"
    print "icon: fa-keyboard-o"
    print "parent: %s Keycaps" % keycapstype
    print "nav_order: %d" % navOrder
    print "---"
    print ""
    print "# %s %s" % (name, cname)
    print ""
    print "ref link: [%s %s GB Link](%s)" % (name, platform, link)
    print ""
    print "* [Price](#price)"
    print "* [Kits](#kits)"
    print "* [Info](#info)"
    print "* [Pictures](#pictures)"
    print ""
    print ""
    print "## Price  "
else:
    print "---"
    print "title: %s" % (name)
    print "layout: default"
    print "icon: fa-keyboard-o"
    print "parent: %s Keycaps" % keycapstype
    print "nav_order: %d" % navOrder
    print "---"
    print ""
    print "# %s" % (name)
    print ""
    print "ref link: [%s %s GB Link](%s)" % (name, platform, link)
    print ""
    print "* [Price](#price)"
    print "* [Kits](#kits)"
    print "* [Info](#info)"
    print "* [Pictures](#pictures)"
    print ""
    print ""
    print "## Price  "

if rate:
    print 'NOTE: USD to RMB exchange rate is %.2f' % rate

# generate price table
    print """
| Name          | Price(%s)    |  Price(RMB) | Quantity |
| ------------- | ------------ |  ---------- | -------- |""" % platform

for i in priceDict:
    # check USD
    if isinstance(priceDict[i][1], float):
        printPriceFormat = "|[%s](#%s)|%.2f|"
        printKitFormat = "**Price(%s):** %.2f    "
    else:
        printPriceFormat = "|[%s](#%s)|%s|"
        printKitFormat = "**Price(%s):** %s    "

    # check RMB
    if isinstance(priceDict[i][2], float):
        printPriceFormat = printPriceFormat + "%.2f|"
        printKitFormat = printKitFormat + "**Price(RMB):** %.2f    "
    else:
        printPriceFormat = printPriceFormat + "%s|"
        printKitFormat = printKitFormat + "**Price(RMB):** %s    "

    # check Quantity
    if hasQuantity:
        if isinstance(priceDict[i][3], int):
            printPriceFormat = printPriceFormat + "%d|"
            printKitFormat = printKitFormat + "**Quantity:** %d  "
        else:
            printPriceFormat = printPriceFormat + "%s|"
            printKitFormat = printKitFormat + "**Quantity:** %s  "

    if hasQuantity:
        print printPriceFormat % (priceDict[i][0], priceDict[i][0].lower().replace(" ","-"), priceDict[i][1], priceDict[i][2], priceDict[i][3])
    else:
        print printPriceFormat % (priceDict[i][0], priceDict[i][0].lower().replace(" ","-"), priceDict[i][1], priceDict[i][2], 'unknown')

priceRelFilePath = 'assets/images/%s-keycaps/%s/price.jpg' % ( keycapstype.lower(), name.lower().replace(" ","") )
priceAbsFilePath = os.path.join('/home/jzou/keyboard/web', priceRelFilePath)
if os.path.isfile(priceAbsFilePath):
    print ''
    print '<img src="{{ \'assets/images/%s-keycaps/%s/price.jpg\' | relative_url }}" alt="price" class="image featured">' % (keycapstype.lower(), name.lower().replace(" ",""))

print ''
print ''

print '## Kits'
for i in priceDict:
    print '### %s' % priceDict[i][0]
    if hasQuantity:
        print printKitFormat % ( platform, priceDict[i][1], priceDict[i][2], priceDict[i][3])
    else:
    	print printKitFormat % (priceDict[i][1], priceDict[i][2], platform, 'unknown')

    kitPicPath = '/home/jzou/keyboard/web/assets/images/%s-keycaps/%s/kits_pics/' % (keycapstype.lower(), name.lower().replace(" ",""))
    if os.path.isdir(kitPicPath):
        pictures = [f for f in listdir(kitPicPath)]
        try:
            kitPic = [p for p in pictures if not p.find(priceDict[i][0].lower().replace(" ","-"))]
            imagePrintFormat = "<img src=\"{{ 'assets/images/%s-keycaps/%s/kits_pics/%s' | relative_url }}\" alt=\"%s\" class=\"image featured\">"
            print imagePrintFormat % (keycapstype.lower(), name.lower().replace(" ",""), kitPic[0], priceDict[i][0])
        except IndexError:
            imagePrintFormat = "<img src=\"{{ 'assets/images/%s-keycaps/%s/kits_pics/%s.png' | relative_url }}\" alt=\"%s\" class=\"image featured\">"
            print imagePrintFormat % (keycapstype.lower(), name.lower().replace(" ",""), priceDict[i][0].lower().replace(" ","-"), priceDict[i][0])
    print ''

print ''
    
# 
# generate info part
#
print """## Info
* Designer: %s
* Profile: %s %s""" % (designer, keycapstype, profile)
print "* GB Time: %s" % time
if keycapstype == "SA" and colorcodes != '' :
    print "* Color Codes: %s  " % (colorcodes)
    for color in colorcodes.split('/'):
        print '<img src="{{ \'assets/images/sa-keycaps/SP_ColorCodes/abs/SP_Abs_ColorCodes_%s.png\' | relative_url }}" alt="color%s" height="150" width="340">' % (color, color)
elif keycapstype == "SA" and colorcodes == '' :
    print "* Color Codes: unknown  "
elif keycapstype == "GMK" :
    print "* ColorCodes: %s " % (colorcodes)
print ''
print ''

#
# generate picture part
#
picPath = '/home/jzou/keyboard/web/assets/images/%s-keycaps/%s/rendering_pics/' % (keycapstype.lower(), name.lower().replace(" ",""))
if os.path.isdir(picPath):
    print '## Pictures'
    pictures = [f for f in listdir(picPath)]
    for pic in pictures:
       print '<img src="{{ \'assets/images/%s-keycaps/%s/rendering_pics/%s\' | relative_url }}" alt="%s" class="image featured">' % ( keycapstype.lower(), name.lower().replace(" ",""), pic, pic.replace(".jpg","") )


# generate index
if cname:
    print "* [%s %s](docs/%s-keycaps/%s/)" % (name, cname, keycapstype.lower(), name.replace(' ','-'))
else:
    print "* [%s](docs/%s-keycaps/%s/)" % (name, keycapstype.lower(), name.replace(' ','-'))

