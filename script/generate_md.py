#! /usr/bin/python

from sys import argv
from os import listdir
import os
from os.path import isfile, join

script, filepath = argv

rateDict = {"2018-11": '6.95', "2018-10": '6.87', "2018-09": '6.95',
    "2018-08": '6.87',"2018-07": '6.67',"2018-06": '6.47',"2018-05": '6.42',
    "2018-04": '6.34',"2018-03": '6.28',"2018-02": '6.29',"2018-01": '6.29', 
    "2017-12": '',"2017-11": '',"2017-10": '',"2017-09": '',
    "2017-08": '',"2017-07": '',"2017-06": '',"2017-05": '',
    "2017-04": '',"2017-03": '',"2017-02": '',"2017-01": '',
    "2016-12": '',"2016-11": '',"2016-10": '',"2016-09": '',
    "2016-08": '',"2016-07": '',"2016-06": '',"2016-05": '',
    "2016-04": '',"2016-03": '',"2016-02": '',"2016-01": '',}

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
rate = float(rateDict[time])

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
keycapPath = '/home/juzou/documents/matrixzj.github.io/docs/%s-keycaps/' % keycapstype.lower()
navOrder = len([eachfile for eachfile in os.listdir(keycapPath) if os.path.isfile(os.path.join(keycapPath, eachfile))]) * 5

# key: name, usd, rmb, proxyprice, quantity
priceDict = {}
sn = 1
for line in lines[9:]:
    kitName = line.split("|")[0]

    kitUSD = line.split("|")[1]
    
    if len(kitUSD) < 1:
        kitUSD = 'unknown'
    else:
        kitUSD = float(kitUSD)

    kitRMB = line.split("|")[2]
    if len(kitRMB) < 1 and isinstance(kitUSD, float):
        kitRMB = float(kitUSD) * rate
    elif len(kitRMB) > 1:
        kitRMB = float(kitRMB)
    else:
	kitRMB = 'unknown'

    kitPlatformPrice = line.split("|")[3]
    if platform:
        if len(kitPlatformPrice) < 1:
            kitPlatformPrice = 'unknown'
        else:
            float(kitPlatformPrice)

    kitQuantity = line.split("|")[4]
    if len(kitQuantity) < 1:
        kitQuantity = 'unknown'
    else:
        int(kitQuantity)

    priceDict[sn] = [kitName, kitUSD, kitRMB, kitPlatformPrice, kitQuantity]
    sn += 1

print "---\ntitle: %s %s\nlayout: default\nicon: fa-keyboard-o\nparent: %s Keycaps\nnav_order: %d\n---\n\n# %s %s\n\nref link: [%s %s GB Link](%s)\n\n* [Price](#price)\n* [Kits](#kits)\n* [Info](#info)\n* [Pictures](#pictures)\n\n\n## Price  " % (name, cname, keycapstype, navOrder, name, cname, name, platform, link)

if rate:
    print 'NOTE: USD to RMB exchange rate is %.2f' % rate

# generate price table
if platform: 
    print """
| Name          | Price(USD)    |  Price(RMB) |  Price(%s) | Quantity |
| ------------- | ------------- |  ---------- |  --------- | -------- |""" % platform
else:
    print """
| Name          | Price(USD)    |  Price(RMB) |  Quantity |
| ------------- | ------------- |  ---------- |  -------- |"""

for i in priceDict:
    # check USD
    if isinstance(priceDict[i][1], float):
        printFormat = "|[%s](#%s)|%.2f|"
    else:
        printFormat = "|[%s](#%s)|%s|"

    # check RMB
    if isinstance(priceDict[i][2], float):
        printFormat = printFormat + "%.2f|"
    else:
        printFormat = printFormat + "%s|"

    # check PlateformPrice
    if platform: 
        if isinstance(priceDict[i][3], str):
            printFormat = printFormat + "%.2f|"
        else:
            printFormat = printFormat + "%s|"

    # check Quantity
    if isinstance(priceDict[i][4], int):
        printFormat = printFormat + "%d|"
    else:
        printFormat = printFormat + "%s|"

    print printFormat
    if platform: 
	print printFormat % (priceDict[i][0], priceDict[i][0].lower().replace(" ",""), priceDict[i][1], priceDict[i][2], float(priceDict[i][3]), priceDict[i][4])
    else:
	print printFormat % (priceDict[i][0], priceDict[i][0].lower().replace(" ",""), priceDict[i][1], priceDict[i][2],  priceDict[i][4])


priceRelFilePath = 'assets/images/%s-keycaps/%s/price.jpg' % ( keycapstype, name.lower().replace(" ","") )
priceAbsFilePath = os.path.join('/home/juzou', priceRelFilePath)
if os.path.isfile(priceAbsFilePath):
    print ''
    print '<img src="{{ \'assets/images/%s-keycaps/%s/price.jpg\' | relative_url }}" alt="price" class="image featured">' % (keycapstype, name.lower().replace(" ",""))

print ''
print ''

print '## Kits'
for i in priceDict:
    print '### %s' % priceDict[i][0]

    # check USD
    if isinstance(priceDict[i][1], float):
        printFormat = "**Price(USD):** %.2f    "
    else:
        printFormat = "**Price(USD):** %s    "

    # check RMB
    if isinstance(priceDict[i][2], float):
        printFormat = printFormat + "**Price(RMB):** %.2f    "
    else:
        printFormat = printFormat + "**Price(RMB):** %s    "

    # check platformPrice
    if platform: 
        if isinstance(priceDict[i][3], str):
	    printFormat = printFormat + "**Price(%s):** %.2f    "
        else:
	    printFormat = printFormat + "**Price(%s):** %s    "

    # check Quantity
    if isinstance(priceDict[i][4], int):
        printFormat = printFormat + "**Quantity:** %d"
    else:
        printFormat = printFormat + "**Quantity:** %s"

    if platform:
	print printFormat % (priceDict[i][1], priceDict[i][2], platform, float(priceDict[i][3]), priceDict[i][4])
    else:
	print printFormat % (priceDict[i][1], priceDict[i][2], priceDict[i][4])
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
print ''
print ''

#
# generate picture part
#
picPath = '/home/juzou/documents/matrixzj.github.io/assets/images/%s-keycaps/%s/rendering_pics/' % (keycapstype.lower(), name.lower().replace(" ",""))
if os.path.isdir(picPath):
    print '## Pictures'
    pictures = [f for f in listdir(picPath)]
    for pic in pictures:
       print '<img src="{{ \'assets/images/%s-keycaps/%s/rendering_pics/%s\' | relative_url }}" alt="%s" class="image featured">' % ( keycapstype.lower(), name.lower().replace(" ",""), pic, pic.replace(".jpg","") )


# generate index
print "* [%s %s](docs/%s-keycaps/%s/)" % (name, cname, keycapstype.lower(), name.replace(' ','-'))

