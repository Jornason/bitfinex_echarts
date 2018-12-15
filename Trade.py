from datetime import datetime, timedelta
import time
import pandas as pd
from email.mime.text import MIMEText
from smtplib import SMTP
import pytz
from utility import run_function_till_success
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 1000)
tz = pytz.timezone('Asia/Shanghai') #东八区


# 获取bitfinex的k线数据
def get_bitfinex_candle_data(exchange, symbol, time_interval, since = 0, limit=1000):
    print("get_bitfinex_candle_data")
    content = exchange.fetch_ohlcv(symbol, timeframe=time_interval, since=since, limit=limit)
    # 整理数据
    df = pd.DataFrame(content, dtype=float)
    df.rename(columns={0: 'MTS', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}, inplace=True)
    df['candle_begin_time'] = pd.to_datetime(df['MTS'], unit='ms')
    df['candle_begin_time_GMT8'] = df['candle_begin_time'] + timedelta(hours=8)
    df = df[['candle_begin_time_GMT8', 'open', 'high', 'low', 'close', 'volume']]
    return df

def transfer_to_period_data(df, rule_type='15T'):
    """
    将数据转换为其他周期的数据
    :param df:
    :param rule_type:
    :return:
    """

    # =====转换为其他分钟数据
    period_df = df.resample(rule=rule_type, on='candle_begin_time', label='left', closed='left').agg(
        {'open': 'first',
         'high': 'max',
         'low': 'min',
         'close': 'last',
         'volume': 'sum',
         })
    period_df.dropna(subset=['open'], inplace=True)  # 去除一天都没有交易的周期
    period_df = period_df[period_df['volume'] > 0]  # 去除成交量为0的交易周期
    period_df.reset_index(inplace=True)
    df = period_df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume']]

    return df

def calcBolling(df,n,m):
    df = df.copy()
    # 计算均线
    df['median'] = df['close'].rolling(n, min_periods=1).mean()

    # 计算上轨、下轨道
    df['std'] = df['close'].rolling(n, min_periods=1).std(ddof=0)  # ddof代表标准差自由度
    df['upper'] = df['median'] + m * df['std']
    df['lower'] = df['median'] - m * df['std']
    return df

def calcEMA(df,n):
    df = df.copy()
    # 计算均线
    df['ema'] = pd.Series.ewm(df['close'], span=n, min_periods=1).mean()
    df['ema'].fillna(value=0, inplace=True)  
    return df['ema']


def calcSince(sinceDt):
    sinceDt=sinceDt
    since = int(time.mktime(time.strptime(sinceDt, "%Y-%m-%d %H:%M:%S")))*1000 + 60 * 1000
    return since


