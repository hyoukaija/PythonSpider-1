import urllib.request
from urllib.request import Request
from urllib.error import HTTPError
from urllib.error import URLError
from fake_useragent import UserAgent
import json
from urllib.parse import urlencode

# 热评地址
base_url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_{id}?csrf_token='
user_agent = UserAgent()

data = {
    'params':'VeixgdOB1izrFDHrhZ3UFjBWjZtqq/I/hU2N3qliM81ZPHgHJe0jlucqsP6o+PpLuEvtnUal5erYncZNCOhEHDNACkW+O2e92LyxH/HWq7auA9qVfcRoVTCjOKzQl37osUCfOgJNIxBT8O/mg6pv8vI7I29U8NB0qO3ifmE+9lPMGtNL8eE61uV7YY1y/g6R',
    'encSecKey':'ad836174e69e218deb13b80ff90c7c6fec0120adfdafd03c085ae00dfe5eb771c003f44562d45775808aaaf47be25bab459e830321e1bc053f8d830f5e9c0b8e53c1be197cb1d0fee13e73ba69bb09e7091229deb7700d8e60e97ce764355172fb2802834e3f9dd28661165bba102c70040f1968ff3cf8b9fc304f91b2f195ce'
}
data = urlencode(data).encode('utf-8')

# 获取json数据
def get_json(url):
    headers = {
        'User-Agent': user_agent.random
    }
    request = Request(url, headers=headers, data=data)
    try:
        response = urllib.request.urlopen(request)
    except HTTPError as e:
        print(e.reason)
    except URLError as e:
        print(e.reason)
    else:
        return json.loads(response.read().decode('utf-8'))

# 提取热评
def parse_json(json):
    if 'hotComments' in json.keys():
        hotComments = json.get('hotComments')
        if hotComments:
            for item in hotComments:
                yield item.get('content')

# 保存至文件
def save_to_flie(item, filename):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(item)

if __name__ == "__main__":
    FLAG = True
    while FLAG:
        song_name = input('请输入歌曲名：')
        song_id = input('请输入该歌曲id：')
        json = get_json(base_url.format(id=song_id))
        filename = '{dictionary}/{name}.txt'.format(dictionary='Comments', name=song_name)
        for item in parse_json(json):
            save_to_flie(item+'\n\n', filename)
        print('爬完了哈！')
        answer = input('还行继续吗？[y/n]')
        if answer.lower() == 'n':
            FLAG = False
