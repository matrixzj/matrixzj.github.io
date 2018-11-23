#! /usr/bin/python

from sys import argv
from os import listdir
import os
from os.path import isfile, join

script, filepath = argv

lines = tuple(open(filepath, 'r'))

# get Name
name = lines[0].split("'")[1]

# get cName
cname = lines[1].split("'")[1]

# get keycaptype
keycapstype = lines[2].split("'")[1]

# get rate
if lines[3].split("'")[1]:
    rate = float(lines[3].split("'")[1])
else:
    rate = ""

# get designer
designer = lines[4].split("'")[1]

# get profile
profile = lines[5].split("'")[1]

# get time
time = lines[6].split("'")[1]

# get colorcodes
colorcodes = lines[7].split("'")[1]

# get plateform
platform = lines[8].split("'")[1]

# get link
link = lines[9].split("'")[1]

# generate navOrder
keycapPath = '/home/juzou/documents/matrixzj.github.io/docs/%s-keycaps/' % keycapstype.lower()
navOrder = len([eachfile for eachfile in os.listdir(keycapPath) if os.path.isfile(os.path.join(keycapPath, eachfile))]) - 1

# key: name, usd, rmb, proxyprice, quantity
priceDict = {}
sn = 1
for line in lines[10:]:
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
        if isinstance(priceDict[i][3], float):
            printFormat = printFormat + "%.2f|"
        else:
            printFormat = printFormat + "%s|"

    # check Quantity
    if isinstance(priceDict[i][4], int):
        printFormat = printFormat + "%d|"
    else:
        printFormat = printFormat + "%s|"

    if platform: 
	print printFormat % (priceDict[i][0], priceDict[i][0].lower().replace(" ",""), priceDict[i][1], priceDict[i][2], priceDict[i][3], priceDict[i][4])
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
        if isinstance(priceDict[i][3], float):
	    printFormat = printFormat + "**Price(%s):** %.2f    "
        else:
	    printFormat = printFormat + "**Price(%s):** %s    "

    # check Quantity
    if isinstance(priceDict[i][4], int):
        printFormat = printFormat + "**Quantity:** %d"
    else:
        printFormat = printFormat + "**Quantity:** %s"

    if platform:
	print printFormat % (priceDict[i][1], priceDict[i][2], platform, priceDict[i][3], priceDict[i][4])
    else:
	print printFormat % (priceDict[i][1], priceDict[i][2], priceDict[i][4])
    imagePrintFormat = "<img src=\"{{ 'assets/images/%s-keycaps/%s/kits_pics/%s.jpg' | relative_url }}\" alt=\"%s\" class=\"image featured\">"
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

