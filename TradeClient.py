import sys
from datetime import datetime, timedelta
import pandas as pd
from time import sleep
import ccxt
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
import pytz
import time
import requests
import json
from utility import run_function_till_success
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
tryTimes   = int(config['default']['tryTimes']) 



class TradeClient:
    """
    Authenticated client for trading through Bitfinex API
    """
    def __init__(self, time_interval='15m', setProxy=True):
        print('__init__')
        self.setProxy = setProxy
        self.URL = 'https://api.bitfinex.com/v1'
        self.bitfinex2 = ccxt.bitfinex2()  # 创建交易所，此处为bitfinex v2 协议
        self.bitfinex1 = ccxt.bitfinex()  # 创建交易所，此处为bitfinex v1 协议
        self.time_interval = time_interval
        self.proxies = {
                "http": "socks5h://127.0.0.1:1080",
                "https": "socks5h://127.0.0.1:1080"
            }
        if self.setProxy:
            self.bitfinex2.proxies = self.proxies
            self.bitfinex1.proxies = self.proxies


    def milliseconds(self):
        since = None
        result = run_function_till_success(function=lambda: self.bitfinex1.milliseconds() , tryTimes=tryTimes)
        if result:
            since = result[0]
            return since
        else:
            raise str(tryTimes) + '次尝试获取失败，请检查网络以及参数'   
            