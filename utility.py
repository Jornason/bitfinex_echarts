import json
import datetime
import requests


def loadJson(filename):
    with open(filename, 'r', encoding='UTF-8') as f:
        data = json.load(f)
        return data

def saveJson(filename, data):
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


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


