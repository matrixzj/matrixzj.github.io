#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
# from os import listdir
# import os
# from os.path import isfile, join
import json
import requests

raw_data_file = sys.argv[1]
# month = sys.argv[2]

class GenerateKeyCapPage(object):
    
    def __init__(self, keycap_raw_info_file):

        self.info_dict = {"price":{}}

        self.parse_keycap_raw_info(keycap_raw_info_file)
#        self.retrieve_exchange_rate()
        self.info_dict['rate'] = 7.16

        print self.info_dict

        self.parse_price_info()
        print self.info_dict

        self.cal_nav_order()

    def parse_keycap_raw_info(self, keycap_info_file):
        lines = open(keycap_info_file, 'r').readlines()
        for line in lines:
            if len(line) <= 1:
                continue
            else:
                if "|" in line:
                    self.info_dict["price"][line.split(":")[0]] = line.split(":")[1].strip().split("|")
                elif "link" in line:
                    self.info_dict["link"] = line.replace("link:","").replace("'","").strip()
                else:
                    self.info_dict[line.split(":")[0]] = line.split(":")[1].replace("'","").strip()

    def retrieve_exchange_rate(self):
        api_base_url = "http://www.apilayer.net/api/historical?format=1"
        
        f_api_file = open('../exchangerate_apikey', 'r')
        exchange_rate_api_key = "access_key=" + f_api_file.read().strip()
        f_api_file.close()
        
        currency_checked = "currencies=%s,CNY" % self.info_dict['currencyunit']
        
        date = "date=%s-01" % self.info_dict['time']
        
        api_url = "%s&%s&%s&%s" % (api_base_url, exchange_rate_api_key, currency_checked, date)

        exchange_rate_result = requests.get(api_url)
        currency_key = "%sCNY" % self.info_dict['currencyunit']
        exchange_rate = exchange_rate_result.json()['quotes'][currency_key]
        self.info_dict['rate'] = "%.2f" % exchange_rate

    def parse_price_info(self):
        for kit in self.info_dict['price']:
            # Price in USD and CNY is Unknown
            if len(self.info_dict['price'][kit][0]) == 0 and \
                len(self.info_dict['price'][kit][1]) == 0:
                self.info_dict['price'][kit][0] = 'Unknown'
                self.info_dict['price'][kit][1] = 'Unknown'
            # Price in USD is provided and CNY is Unkonwn
            elif len(self.info_dict['price'][kit][0]) > 0 and \
                len(self.info_dict['price'][kit][1]) == 0:
                self.info_dict['price'][kit][0] = float(self.info_dict['price'][kit][0])
                self.info_dict['price'][kit][1] = float(self.info_dict['price'][kit][0]) * float(self.info_dict['rate'])
            # Price in CYN is provided and USD is Unkonwn
            elif len(self.info_dict['price'][kit][0]) == 0 and \
                len(self.info_dict['price'][kit][1]) > 0:
                self.info_dict['price'][kit][0] = float(self.info_dict['price'][kit][1]) / float(self.info_dict['rate'])
                self.info_dict['price'][kit][1] = float(self.info_dict['price'][kit][1])
            else:
                self.info_dict['price'][kit][0] = float(self.info_dict['price'][kit][0])
                self.info_dict['price'][kit][1] = float(self.info_dict['price'][kit][1])

            if len(self.info_dict['price'][kit][2]) == 0:
                self.info_dict['price'][kit][2] = 'Unkonwn'
            else:
                self.info_dict['price'][kit][2] = int(self.info_dict['price'][kit][2])

    def cal_nav_order(self):
        fd_index = open("../index.md", "r")
        index_lines = fd_index.readlines()
        fd_index.close()

        profile_list = ['SA', 'GMK', '---']
        profile_current = self.info_dict['keycapstype']

        # Generate Profile Part
        current_profile_index = profile_list.index(profile_current)
        next_profile_index = current_profile_index + 1
        current_profile_marker = "## %s KeyCaps\n" % profile_list[current_profile_index]
        if next_profile_index == len(profile_list):
            next_profile_marker = "%s\n" % profile_list[-1]
        else:
            next_profile_marker = "## %s KeyCaps\n" % profile_list[next_profile_index]
        current_profile_marker_index = index_lines.index(current_profile_marker)
        next_profile_marker_index = index_lines.index(next_profile_marker)
        current_profile_list = index_lines[current_profile_marker_index:next_profile_marker_index]

        # Generate Year Part
        current_year = self.info_dict['time'].split("-")[0]
        previous_year = int(current_year) - 1
        current_year_marker = "### %s\n" % current_year
        if previous_year < 2013:
            previous_year_marker = "---\n"
        else:
            previous_year_marker = "### %d\n" % previous_year
        current_year_marker_index = current_profile_list.index(current_year_marker)
        previous_year_marker_index = current_profile_list.index(previous_year_marker)

        currrent_items_count =  len(current_profile_list[current_year_marker_index:previous_year_marker_index]) - 2


#        line_number = 0
#        while line_number < len(index_lines):
#            if year_marker in index_lines[line_number]:
#                print line_number
#
#            line_number += 1

GenerateKeyCapPage(raw_data_file)
