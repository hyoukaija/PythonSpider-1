import requests
from fake_useragent import UserAgent
import time

user_agent = UserAgent()

headers = {
    "User-Agent": user_agent.random
}

base_url = 'http://neihanshequ.com/joke/?is_json=1&app_name=neihanshequ_web&max_time='
url = 'http://neihanshequ.com/joke/?is_json=1&app_name=neihanshequ_web&max_time='+str(int(time.time()))

for i in range(3):
    time.sleep(1)
    response = requests.get(url, headers=headers)
    for i in range(20):
        content = response.json()['data']['data'][i]['group']['content']
        print(content)
        with open('neihan.txt', 'a', encoding='utf-8') as f:
            f.write(content+'\n\n')
    url = base_url + str(int(response.json()['data']['max_time']))
