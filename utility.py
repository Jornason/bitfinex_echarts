import json
import datetime
import requests

def send_dingding_msg(content,robot_id='824d689cd23a7ab433561df1ddabf8dc914504d4c2b1e1da2b584c4f543eb2d2'):
    try:
        msg={
            "msgtype":"text",
            "text":{
                "content":content+'\n'+datetime.datetime.now().strftime("%m-%d %H:%M:%S")
                }
            }
        Headers={
            "Content-Type":"application/json;charset=utf-8"
        }
        url='https://oapi.dingtalk.com/robot/send?access_token='+robot_id
        body=json.dumps(msg)
        res = requests.post(url,data=body,headers=Headers)
        print(res)
    except Exception as err:
        print('钉钉发送失败',err)

def loadJson(filename):
    with open(filename, 'r', encoding='UTF-8') as f:
        data = json.load(f)
        return data

def saveJson(filename, data):
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


# result = run_function_till_success(function=lambda: ccxt_get_bitfinex_latest_k_data(timeframe=timeframe), tryTimes=tryTimes)

def run_function_till_success(function, tryTimes=5):
    '''
    将函数function尝试运行tryTimes次，直到成功返回函数结果和运行次数，否则返回False
    '''
    retry = 0
    while True:
        if retry > tryTimes:
            return False
        try:
            result = function()
            return [result, retry]
        except:
            retry += 1


