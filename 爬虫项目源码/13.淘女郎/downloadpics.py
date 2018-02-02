import requests
from pymongo import MongoClient
import os.path
from fake_useragent import UserAgent


client = MongoClient()
db = client['Girls']
coll = db['TaoGirls']

user_agent = UserAgent()


def getData(url):
    headers = {'User-Agent': user_agent.random}
    try:
        response = requests.get(url, headers=headers)
        data = response.content
    except:
        data = None
    return data


def download(data, path):
    if data:
        with open(path, 'wb') as f:
            f.write(data)

if __name__ == "__main__":
    for i in coll.find():
        url = i['avatarUrl']
        if url:
            absurl = 'http:' + url
            path = os.path.join("Images", url.split('/')[-1])
            data = getData(absurl)
            print(absurl)
            download(data, path)