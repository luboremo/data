#!/usr/bin/env python2

'''
Creates a csv file with timestamp and current Cointracking account balance. 
Append account balance value every 15 minutes.
'''

from ctapi import CTAPI
import pandas as pd
from datetime import datetime
import time, sched

api_key = ''
api_secret = ''
api = CTAPI(api_key, api_secret)

# Path to csv needs to be set 
def create_the_dataframe():
    balance_data = api.getBalance()
    actual_value = {int(time.time()) : float(balance_data['result']['summary']['profit_fiat'])}
    data_df = pd.DataFrame.from_dict(actual_value, orient='index')
    data_df.rename(columns={0:'EUR'}, inplace=True)
    data_df.to_csv(r'E:/balances1.csv')

# Path to csv needs to be set
def get_actual_balance():        
    balances = pd.read_csv(r'E:/balances1.csv', index_col=0)
    balance_data = api.getBalance()
    actual_value = {int(time.time()) : float(balance_data['result']['summary']['profit_fiat'])}
    data_df = pd.DataFrame.from_dict(actual_value, orient='index')
    data_df.rename(columns={0:'EUR'}, inplace=True)
    balances = balances.append(data_df)
    balances.to_csv(r'E:/balances1.csv')

def update_data():
    starttime = time.time()
    while True:
        get_actual_balance()
        time.sleep(900.0 - ((time.time() - starttime) % 900.0))

create_the_dataframe()        
update_data()
