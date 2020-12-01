import pandas as pd
import requests
import json
from datetime import timezone
import datetime
import time
from dateutil.rrule import rrule, DAILY

'''

Downloads historical data of daily MOVE contracts from FTX.

'''



MOVE_daily_data = pd.DataFrame()
MOVE_tick_daily_data = pd.DataFrame()

dt = datetime.datetime(2019, 12, 31, 0, 0)
dt2 = datetime.datetime(2019, 12, 31, 1, 0)

class API_Client_FTX:

    def __init__(self, symbol, data_granularity):
        self.symbol = symbol
        self.data_granularity = data_granularity
        self.df = self.getData()


    def getData(self):
        base = 'https://ftx.com/api'
        start_time=str(dt.replace(tzinfo=timezone.utc).timestamp())
        end_time=str(dt2.replace(tzinfo=timezone.utc).timestamp())


        params = '/markets/'+self.symbol+'/candles?resolution='+self.data_granularity+'&start_time='+start_time+'&end_time='+end_time

        url = base + params

        data = requests.get(url)
        dictionary = json.loads(data.text)

        correct_dictionary = []
        for x in dictionary['result']:
            correct_dictionary.append([x['time'], x['close'], x['high'], x['low'], x['open'], x['volume']])

        df = pd.DataFrame.from_dict(correct_dictionary)

        col_names = ['time','close','high','low','open','volume']
        df.columns = col_names
        for col in col_names:
            df[col] = df[col].astype(float)
        df.sort_values(by=['time'], inplace=True)
        df['time'] = df['time'] / 1000
        df['time'] = df['time'].apply(lambda x: '%.2f' % x)
        return df

    def plotData(self):
        df = self.df

        candle = go.Candlestick(
            x = df['time'],
            open = df['open'],
            close = df['close'],
            high = df['high'],
            low = df['low'],
            name = "candlesticks")

        data = [candle]

        layout = go.Layout(title = self.symbol)
        fig = go.Figure(data = data, layout = layout)

        plot(fig, filename=self.symbol)

    def export_to_csv(self):
        df = self.df
        return df.to_csv(r'<PATH TO FILE>\\'+str(self.symbol)+r'.csv')

# create list of dates for contract name specification
dates_list = []
days_range = rrule(DAILY, dtstart=(dt + datetime.timedelta(days=1)), until=(dt2 + datetime.timedelta(days=1)))

for dts in days_range:
    dates_list.append(dts.strftime("%m%d"))
    #print(dates_list)


# main function to run the whole process
def hist_tick_MOVE_data():
    global dates_list, dt, dt2, MOVE_tick_daily_data
    for d in dates_list:
        individual_file = pd.DataFrame()
        hours = list(range(0,48))
        for h in hours:
            symbol = 'BTC-MOVE-'+d
            data_granularity = '15'
            client = API_Client_FTX(symbol, data_granularity)
            temp_data = client.getData()
            individual_file = individual_file.append(temp_data)
            MOVE_tick_daily_data = MOVE_tick_daily_data.append(temp_data)
            dt +=  datetime.timedelta(hours=1)
            dt2 += datetime.timedelta(hours=1)
            individual_file.to_csv(r'<PATH TO FILE>\\'+str(symbol)+r'.csv')
            print(str(h+1) + ' hours of data from ' + '' + symbol + ' downloaded.')
            time.sleep(1)
        print('Data of MOVE-' + d + ' downloaded.')
    MOVE_tick_daily_data.to_csv(r'<PATH TO FILE>\\MOVE_tick_data.csv')


hist_tick_MOVE_data()
