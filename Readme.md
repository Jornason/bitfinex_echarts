
## 运行方式
python bitfinex_echarts_server.py


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



## 文件说明
config.ini : 配置参数文件
btc_5min_data1.csv : btc历史数据(可自行更新)
eth_5min_data1.csv : eth历史数据(可自行更新)



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
