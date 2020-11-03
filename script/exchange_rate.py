#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import requests

API_BASE_URL = "http://www.apilayer.net/api/historical?format=1"

f_api_file = open('exchangerate_apikey', 'r')
EXCHANGE_RATE_API_KEY = "access_key=" + f_api_file.read().strip()
f_api_file.close()

def retrieve_exchange_rate(date, currency = 'USD'):
    
    check_date = "date=%s" % date

    currency_checked = "currencies=%s,CNY,%s" % ("USD", currency)
    api_url = "%s&%s&%s&%s" % (API_BASE_URL, EXCHANGE_RATE_API_KEY, currency_checked, check_date)
    exchange_rate_result = requests.get(api_url)
    currency_key_USDtoCNY = "USDCNY"
    currency_key_USDtoDest = "USD%s" % currency
    exchange_rate = float(exchange_rate_result.json()['quotes'][currency_key_USDtoCNY]) / float(exchange_rate_result.json()['quotes'][currency_key_USDtoDest])

    return exchange_rate

if __name__ == '__main__':
    rate = retrieve_exchange_rate('2020-11-02', 'GBP')
    print(rate)
