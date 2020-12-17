#!/usr/bin/env python2
from ctapi import CTAPI
import pandas as pd
from datetime import datetime
import time
from pathlib2 import Path

api_key = 'ab3228402f2b778d1d2c960856c06e7f'
api_secret = '8b9c29dbc319b57687dfb71c6467e9e6928e80f740ae4c1a'
api = CTAPI(api_key, api_secret)

def create_data_file():
    api_data = api.getGroupedBalance()
    actual_exchanges = []
    for x in list(api_data['result']['details'].keys()): 
        actual_exchanges.append(x)
    actual_value = []
    for x in list(api_data['result']['details'].keys()): 
        actual_value.append(api_data['result']['details'][x]['TOTAL_SUMMARY']['fiat'])
    filtered_dict = {"Exchange": actual_exchanges, int(time.time()): actual_value}

    data_df = pd.DataFrame.from_dict(test_dict, orient='columns')
    data_df.set_index("Exchange").transpose()
    data_df.to_csv(r'C:\Users\lubor\Documents\Projects\additional_files\test_data\balances_by_exchange.csv')

def get_actual_balances():
    balances = pd.read_csv(r'C:\Users\lubor\Documents\Projects\additional_files\test_data\balances_by_exchange.csv', index_col=0)
    api_data = api.getGroupedBalance()
    actual_exchanges = []
    for x in list(api_data['result']['details'].keys()): 
        actual_exchanges.append(x)
    actual_value = []
    for x in list(api_data['result']['details'].keys()): 
        actual_value.append(api_data['result']['details'][x]['TOTAL_SUMMARY']['fiat'])
    filtered_dict = {"Exchange": actual_exchanges, int(time.time()): actual_value}
    data_df = pd.DataFrame.from_dict(test_dict, orient='columns')
    data_df.set_index("Exchange", inplace=True).transpose()
    balances = balances.append(data_df)
    balances.to_csv(r'C:\Users\lubor\Documents\Projects\additional_files\test_data\balances_by_exchange.csv')


def update_data():
    starttime = time.time()
    while True:
        get_actual_balances()
        print('Balances by exchange last checked at' + ' ' + datetime.utcfromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
        time.sleep(900.0 - ((time.time() - starttime) % 900.0))
