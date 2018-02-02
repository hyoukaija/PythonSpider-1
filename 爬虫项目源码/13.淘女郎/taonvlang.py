from fake_useragent import UserAgent
import requests
from pymongo import MongoClient
import time

client = MongoClient()
db = client['Girls']
coll = db['TaoGirls']

base_url = 'https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8'

user_agent = UserAgent()


# 得到JSON数据
def getData(pageNum):
    formdata = {'currentPage': pageNum, 'viewFlag': 'A'}
    headers = {'User-Agent': user_agent.random}
    try:
        response = requests.post(base_url, headers=headers, data=formdata)
    except:
        return None
    data = response.json()['data']['searchDOList']
    return data


# 保存到数据库
def saveToDB(items):
    coll.insert_many(items)


if __name__ == "__main__":
    for pageNum in range(1, 1451):
        items = getData(str(pageNum))
        if items:
            saveToDB(items)
        time.sleep(1)