#!/usr/bin/env python
#-*- coding: utf-8 -*-

from sys import argv
import json
import os
import re

import exchange_rate
import download_graph
import resize_pic

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

SPACELINE = '\n'

PROFILES = ['SA', 'GMK', 'DSA', '---']

keycap_raw_info_file = argv[1]

# load info form raw file 
with open(keycap_raw_info_file) as json_file:
    info_dict = json.load(json_file)

# Example: GodSpeed-R2
KEYCAP_NAME = info_dict['name'].replace(" ","-").replace("/", "-")
# Example: sa-keycaps
PROFILE_PATH = info_dict['keycapstype'].lower() + "-keycaps"
# Example: GodSpeed-R2.md
KEYCAP_FILENAME = KEYCAP_NAME + ".md"
# Example: docs/sa-keycaps/GodSpeed-R2.md
KEYCAP_FILENAME_WITH_PATH = os.path.join("docs", PROFILE_PATH, KEYCAP_FILENAME)
# Example: assets/images/sa-keycaps/GodSpeed-R2
KEYCAP_ASSETS_WITH_PATH = os.path.join("assets/images", PROFILE_PATH, KEYCAP_NAME)

info_dict['rate'] = exchange_rate.retrieve_exchange_rate(info_dict['time'].split('~')[0].strip())

def write_to_file(string):
    fd = open(KEYCAP_FILENAME_WITH_PATH, 'ab')
    fd.write(string)
    fd.close()

def read_nav_order(filename):
    fd = open(filename, "r")
    file_lines = fd.readlines()
    for line in file_lines:
        if "nav_order" in line:
	    return int(line.split(":")[1].strip())

def cal_nav_order(keycapType):
    fd_index = open("index.md", "r")
    index_lines = fd_index.readlines()
    fd_index.close()

    if os.path.isfile(KEYCAP_FILENAME_WITH_PATH):
	info_dict['nav_order'] = read_nav_order(KEYCAP_FILENAME_WITH_PATH)
    else:
        current_profile_marker = '## {} KeyCaps\n'.format(keycapType)
	current_porfile_index = index_lines.index(current_profile_marker)

	year_marker = '### {}\n'.format(info_dict['time'].split('-')[0])
	year_index = index_lines.index(year_marker, current_porfile_index)

	latest_entry = index_lines[year_index + 1]
	latest_file_name = '{}.md'.format(re.sub(".*\(", "", latest_entry)[:-3])
	current_nav_order = read_nav_order(latest_file_name)
	info_dict['nav_order'] = current_nav_order - 5

def parse_price_info_format():
    for kit in info_dict['price_list']:
	if kit['price']:
             kit['price'] = '{:.2f}'.format(float(kit['price']))
	else:
	    if kit['price_cny']:
		kit['price'] = '{:.2f}'.format(float(kit['price_cny']) / float(info_dict['rate']))
	    else:
		kit['price'] = 'Unknown'

	if kit['price_cny']:
             kit['price_cny'] = '{:.2f}'.format(float(kit['price_cny']))
	else:
	    if kit['price']:
		kit['price_cny'] = '{:.2f}'.format(float(kit['price']) * float(info_dict['rate']))
	    else:
		kit['price_cny'] = 'Unknown'

         # Quantity is Unknown
        if kit['quantity']:
            kit['quantity'] = int(kit['quantity'])
        else:
            kit['quantity'] = 'Unknown'

def generate_keycap_page_start():
    if os.path.isfile(KEYCAP_FILENAME_WITH_PATH):
        tmp_file_name = os.path.join("/tmp", "%s.md" % KEYCAP_NAME)
        os.rename(KEYCAP_FILENAME_WITH_PATH, tmp_file_name)

def generate_keycap_page_header():
    keycap_page_header = """---
title: {} {}
layout: default
icon: fa-keyboard-o
parent: {} Keycaps
nav_order: {}
---
""".format(info_dict['name'], info_dict['cname'].encode('utf-8'), info_dict['keycapstype'], info_dict['nav_order'])
    write_to_file(keycap_page_header)

def generate_graph_info(url, sub_path, name):
    path = os.path.join(KEYCAP_ASSETS_WITH_PATH, sub_path)
    if not os.path.isdir(path):
        os.makedirs(path)
    graph_path = download_graph.download_graph(url, KEYCAP_ASSETS_WITH_PATH, sub_path, name)
    resize_pic.resize_file(graph_path)
    graph_info = """<img src=\"{{{{ '{}' | relative_url }}}}\" alt=\"{}\" class=\"image featured\">
""".format(os.path.relpath(graph_path, os.getcwd()), name)
    return graph_info

def generate_keycap_page_index():
    keycap_page_title = """
# {} {}
""".format(info_dict['name'], info_dict['cname'].encode('utf-8'))
    write_to_file(keycap_page_title)

    keycap_page_index = """
ref link: [{} {} GB Link]({})

* [Price](#price)
* [Kits](#kits)
* [Info](#info)
* [Pictures](#pictures)""".format(info_dict['name'], info_dict['platform'], info_dict['link'])
    write_to_file(keycap_page_index)
 
def generate_keycap_page_price():
    parse_price_info_format()

    keycap_page_price_header = """

## Price

NOTE: USD to CNY exchange rate is {:.2f}
""".format(info_dict['rate'])
    write_to_file(keycap_page_price_header)

    keycap_page_price_table_header = """
| Name          | Price({})   |  Price(CNY) | Quantity |
| ------------- | ------------ |  ---------- | -------- |""".format(info_dict['currencyunit'])
    write_to_file(keycap_page_price_table_header)

    for kit in info_dict['price_list']:
	keycap_page_price_table_entry = """
|[{}](#{})|{}|{}|{}|""".format(kit['name'], kit['name'].lower().replace(" ", "-").replace(".", ""), kit['price'], kit['price_cny'], kit['quantity'])
	write_to_file(keycap_page_price_table_entry)

    write_to_file(SPACELINE)
    write_to_file(SPACELINE)

    if info_dict["price_pic"]:
	keycap_page_price_price_graph_info = generate_graph_info(info_dict['price_pic'], '', 'price')
	write_to_file(keycap_page_price_price_graph_info)	

    if info_dict["history_graph"]:
	keycap_page_price_history_graph_info = generate_graph_info(info_dict['history_graph'], '', 'history')
	write_to_file(keycap_page_price_history_graph_info)	

    if info_dict["order_graph"]:
	keycap_page_price_order_graph_info = generate_graph_info(info_dict['order_graph'], '', 'order')
	write_to_file(keycap_page_price_order_graph_info)	

    write_to_file(SPACELINE)

def generate_keycap_page_kit():
    keycap_page_kit_title = '## Kits\n'
    write_to_file(keycap_page_kit_title)

    for kit in info_dict['price_list']:
	if kit['pic']:
	    keycap_page_kit_entry_graph_info = generate_graph_info(kit['pic'], 'kits_pics', kit['name'].lower().replace(' ', '-'))
	else:
	    keycap_page_kit_entry_graph_info = ''

	keycap_page_kit_entry = """### {}  
**Price({}):** {}	**Price(CNY):** {}	**Quantity:** {}  
{}
""".format(kit['name'], info_dict['currencyunit'], kit['price'], kit['price_cny'], kit['quantity'], keycap_page_kit_entry_graph_info)
	write_to_file(keycap_page_kit_entry)

def generate_keycap_page_info():
    keycap_page_info_header = """## Info
* Designer: {}  
* Profile: {} {}  
* GB Time: {}  
* Color Codes:  
""".format(info_dict['designer'], info_dict['keycapstype'], info_dict['profile'], info_dict['time'])
    write_to_file(keycap_page_info_header)

    if info_dict['keycapstype'] == "SA" and info_dict['colorcodes']:
        write_to_file(SPACELINE)
        keycap_page_info_color_sa_table_header = """<table style="width:100%">
  <tr>
    <th>ColorCodes</th>
    <th>Sample</th>
  </tr>"""
        write_to_file(keycap_page_info_color_sa_table_header)

        for color in info_dict['colorcodes'][0].split('/'):
            keycap_page_info_color_sa_table_entry = """  <tr>
    <th>{}</th>
    <th><img src="{{{{ 'assets/images/sa-keycaps/SP_ColorCodes/abs/SP_Abs_ColorCodes_{}.png' | relative_url }}}}" alt="Color_{}" height="75" width="170"></th>
  </tr>
""".format(color, color, color)
            write_to_file(keycap_page_info_color_sa_table_entry)

        keycap_page_info_color_sa_table_end = '</table>'
        write_to_file(keycap_page_info_color_sa_table_end)

    if info_dict['keycapstype'] == "GMK" and info_dict['colorcodes']:
        keycap_page_info_color_gmk_table_header = """
| |Base Color     | Legend Color
| :-------------: | :-------------: | :------------:
"""
        write_to_file(keycap_page_info_color_gmk_table_header)
        
	for color in info_dict['colorcodes']:
	    write_to_file("{}\n".format(color))

    write_to_file(SPACELINE)

    # generate color graph files
    for index in range(0, len(info_dict['color_pics'])):
        keycap_page_info_color_graph_entry = generate_graph_info(info_dict['color_pics'][index], '', index)
        write_to_file(keycap_page_info_color_graph_entry)

    write_to_file(SPACELINE)

def generate_keycap_page_pics():
    keycap_page_pics_header = '## Pictures  \n'
    write_to_file(keycap_page_pics_header)

    for index in range(0, len(info_dict['render_pics'])):
        keycap_page_pic_entry = generate_graph_info(info_dict['render_pics'][index], 'rendering_pics', index)
        write_to_file(keycap_page_pic_entry)

def generate_keycap_page_end():

    tmp_file_name = os.path.join("/tmp", "%s.md" % KEYCAP_NAME)
    if os.path.isfile(tmp_file_name):
	print bcolors.WARNING + "Diff result:\n" + bcolors.ENDC
        os.system("diff %s %s" % (KEYCAP_FILENAME_WITH_PATH, tmp_file_name))
    else:
	print bcolors.WARNING + "First result:\n" + bcolors.ENDC
        with open(KEYCAP_FILENAME_WITH_PATH) as fd:
            Lines = fd.readlines()
        for line in Lines:
            print("{}".format(line.strip()))
        
    print bcolors.OKGREEN + "{} was generated!".format(KEYCAP_FILENAME_WITH_PATH) + bcolors.ENDC
    if info_dict['cname']:
        index_entry = "* [{} {}](docs/{}-keycaps/{}/)".format(info_dict['name'], info_dict['cname'].encode('utf-8'), info_dict['keycapstype'].lower(), KEYCAP_NAME)
    else:
        index_entry = "* [{}](docs/{}-keycaps/{}/)".format(info_dict['name'], info_dict['keycapstype'].lower(), KEYCAP_NAME)

    print bcolors.OKGREEN + "index entry: " + bcolors.ENDC + index_entry

cal_nav_order(info_dict['keycapstype'])
generate_keycap_page_start()
generate_keycap_page_header()
generate_keycap_page_index()
generate_keycap_page_price()
generate_keycap_page_kit()
generate_keycap_page_info()
generate_keycap_page_pics()
generate_keycap_page_end()
