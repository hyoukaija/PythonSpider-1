import requests
from fake_useragent import UserAgent

user_agent = UserAgent()

base_url = 'https://m.weibo.cn/api/comments/show?id=4189261588387042&page='


for i in range(1, 20):  # 调整页数
    url = base_url + str(i)
    response = requests.get(url, headers={'User-Agent': user_agent.random})
    for i in range(len(response.json()['data']['data'])):
        comment = response.json()['data']['data'][i]['text']
        print(comment)
        with open('weibo.txt', 'a', encoding='utf-8') as f:
            f.write(comment+'\n\n')