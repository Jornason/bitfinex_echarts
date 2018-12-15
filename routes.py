from flask import url_for, request
from util import json_response
import requests
import urllib
import sys
from datetime import datetime, timedelta
import pandas as pd
from time import sleep
import ccxt
from Trade import get_bitfinex_candle_data,transfer_to_period_data,calcBolling,calcSince,calcEMA
from utility import saveJson
import pytz
import time
import json
from pprint import pprint,pformat
from TradeClient import TradeClient
import configparser
import numpy as np
from echarts_data import get_echarts_html
from Signals import signal_moving_average


config = configparser.ConfigParser()
config.read('config.ini')
tz = pytz.timezone('Asia/Shanghai') #东八区
client = TradeClient(setProxy=True)

def routes(app):
    """app routes"""

    @app.route('/')
    def index():
        """index page"""
        print('index')
        r = {}
        return json_response(200, r, True)    
    

    @app.route("/query")
    def query_echarts():
        print('query_log')
        config.read('config.ini')
        rule_type = config['trade']['rule_type']
        real_data  = config['default']['real_data'] #是否需要实时数据，1：需要，其他：不需要           
        symbol  = config['trade']['symbol']               # 交易品种

        forward_num = request.args.get("forward") or ""
        backward_num = request.args.get("backward") or ""
        begin_time = request.args.get("begin_time") or ""
        end_time = request.args.get("end_time") or ""
        trade_symbol    = request.args.get("trade_symbol") or "" 

        filename = config['default']['filename']
        if (trade_symbol != ""):   # 交易品种
            trade_symbol = trade_symbol.upper()
            print(trade_symbol)
            if trade_symbol == 'ETH':
                filename = config['default']['filename_eth']
            elif trade_symbol == 'BTC':
                filename = config['default']['filename_btc']

            symbol = trade_symbol + '/USDT'

        time_forward = int(config['trade']['time_forward'])
        time_interval   = config['trade']['time_interval']  # 间隔运行时间，不能低于5min, 实际 15m
        since = client.milliseconds() - time_forward 
        _all_data = pd.read_csv(filename)

        _all_data = _all_data.sort_values(by='candle_begin_time', ascending=False)
        last_time = _all_data.loc[0, 'candle_begin_time'] # 历史数据文件中，最近的一次时间
        all_data = _all_data.copy()
        all_data['candle_begin_time'] = pd.to_datetime(all_data['candle_begin_time'])
    
        if real_data == "1": # 需要请求实时数据
            df_real = get_bitfinex_candle_data(client.bitfinex1, symbol, time_interval, since=since, limit=1000)
            df_real.rename(columns={'candle_begin_time_GMT8':'candle_begin_time'}, inplace = True)
            df_real['candle_begin_time'] = pd.to_datetime(df_real['candle_begin_time'])
            df_real = df_real.sort_values(by='candle_begin_time', ascending=False)
            df_real = df_real[df_real['candle_begin_time'] > last_time]
            all_data = all_data.append(df_real, ignore_index=True)        

        all_data = all_data.sort_values(by='candle_begin_time', ascending=False)
        all_data = transfer_to_period_data(all_data, rule_type)
        print(all_data.columns.values.tolist())
        _forward_num = 0
        _backward_num = 0
        if (forward_num != ""):   
            _forward_num = int(forward_num)
        if (backward_num != ""):   
            _backward_num = int(backward_num)
        if (begin_time != ""):        
            all_data = all_data[all_data['candle_begin_time'] >= pd.to_datetime(begin_time)]
        if (end_time != ""):        
            all_data = all_data[all_data['candle_begin_time'] <= pd.to_datetime(end_time)]

        all_data.reset_index(inplace=True, drop=True)
        df = all_data.copy() 
        if (forward_num == "" and begin_time == "" and end_time == ""):
            _forward_num = 1000
        if _forward_num != 0:
            df = df.iloc[-_forward_num:]
        if _backward_num != 0:
            df = df.iloc[_backward_num:]
        df['candle_begin_time'] = df['candle_begin_time'].apply(str)
        n       = int(config['param']['n']) 
        m       = float(config['param']['m']) 
        ema_short   = int(config['ema_param']['ema_short']) 
        ema_long   = int(config['ema_param']['ema_long']) 
        df = calcBolling(df,n,m)
        df["ema_short"] = calcEMA(df,ema_short)
        df["ema_long"] = calcEMA(df,ema_long)

        signal = '[],'

        # todo
        # 参考如下写法，替换自己的交易信号函数 
        # df = signal_moving_average(df)  

        _df = df[['candle_begin_time','open','close','low','high']]
        _df_boll = df[['upper','lower','median','volume','ema_short','ema_long']]

        _df_boll['upper'].fillna(value=0, inplace=True)  
        _df_boll['lower'].fillna(value=0, inplace=True)  
        _df_boll['median'].fillna(value=0, inplace=True)  
        _df_list = np.array(_df).tolist()
        _df_boll_list= np.array(_df_boll).transpose().tolist()
        str_df_list = pformat(_df_list)
        str_df_boll_list = pformat(_df_boll_list)

        if 'signal' in df.columns.tolist():
            x = list(df[df['signal'].notnull()]['candle_begin_time'])
            y = list(df[df['signal'].notnull()]['high'])
            z = list(df[df['signal'].notnull()]['signal'])
            signal = '['
            for i in zip(x,y,z):  #rgb(41,60,85)
                if i[2] ==1:
                    temp = "{coord:['"+str(i[0])+"',"+str(i[1]) + "], label:{ normal: { formatter: function (param) { return \"买\";}} } ,itemStyle: {normal: {color: 'rgb(214,18,165)'}}},"
                elif i[2] ==-1:
                    temp = "{coord:['" + str(i[0]) + "'," + str(
                        i[1]) + "] , label:{ normal: { formatter: function (param) { return \"卖\";}} } ,itemStyle: {normal: {color: 'rgb(0,0,255)'}}},"
                else:
                    temp = "{coord:['" + str(i[0]) + "'," + str(
                        i[1]) + "], label:{ normal: { formatter: function (param) { return \"平仓\";}} },itemStyle: {normal: {color: 'rgb(224,136,11)'}}},"

                signal += temp
            signal = signal.rstrip(',')
            signal += '],'

        _html = get_echarts_html(symbol,str_df_list,str_df_boll_list,signal)
        return _html 







