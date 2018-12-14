
## 在线体验
http://144.34.219.181:3002/query?begin_time=2018-12-04&trade_symbol=eth

## 依赖包安装

```
pip install pandas0.22.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install ccxt1.17.490 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install requests2.18.4 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install PyEmail -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install pysocks1.6.6 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install pytz -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install pprint -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 运行方式
```
git clone https://github.com/Jornason/bitfinex_echarts
cd bitfinex_echarts
python bitfinex_echarts_server.py
```




## 文件说明
config.ini : 配置参数文件
btc_5min_data1.csv : btc历史数据(可自行更新)
eth_5min_data1.csv : eth历史数据(可自行更新)

## 买、卖、平仓提示
eth 案例
![image](https://raw.githubusercontent.com/Jornason/bitfinex_echarts/master/images/buy_sell_eth.png)
btc 案例
![image](https://raw.githubusercontent.com/Jornason/bitfinex_echarts/master/images/buy_sell_btc.png)

请自行修改Signals中交易策略函数，工程中提供的signal_moving_average函数仅作为案例不具实际交易意义
signal:1    买入
signal:-1   卖出
signal:0:   平仓



## url 参数说明
### trade_symbol 
交易品种，目前支持ETH, BTC
http://127.0.0.1:3002/query?trade_symbol=eth
![image](https://raw.githubusercontent.com/Jornason/bitfinex_echarts/master/images/trade_symbol_eth.png)

http://127.0.0.1:3002/query?trade_symbol=btc

![image](https://raw.githubusercontent.com/Jornason/bitfinex_echarts/master/images/trade_symbol_btc.png)





### begin_time
开始时间
http://127.0.0.1:3002/query?begin_time=2018-01-01&trade_symbol=eth
![image](https://raw.githubusercontent.com/Jornason/bitfinex_echarts/master/images/begin_time.png)



### end_time
结束时间
http://127.0.0.1:3002/query?begin_time=2018-01-01&end_time=2018-05-01&trade_symbol=eth
![image](https://raw.githubusercontent.com/Jornason/bitfinex_echarts/master/images/end_time.png)


### forward

表示向前多少根k线
http://127.0.0.1:3002/query?forward=1000&trade_symbol=eth
![image](https://raw.githubusercontent.com/Jornason/bitfinex_echarts/master/images/forward.png)


### backward

表示向后多少根k线，可以结合begin_time一起使用
http://127.0.0.1:3002/query?begin_time=2018-01-01&backward=1000&trade_symbol=eth
![image](https://raw.githubusercontent.com/Jornason/bitfinex_echarts/master/images/backward.png)
