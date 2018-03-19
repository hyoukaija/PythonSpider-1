import requests
from fake_useragent import UserAgent
from scrapy.selector import Selector
import MySQLdb

conn = MySQLdb.connect(host='localhost', user='root', passwd='admin', db='IPs', charset="utf8", use_unicode=True)
cursor = conn.cursor()
user_agent = UserAgent()


def crawl_ips():
    # 爬取西刺的免费ip代理
    header = {
        'User-Agent':user_agent.random
    }

    for page in range(1, 2175):
        response = requests.get('http://www.xicidaili.com/nn/{0}'.format(page), headers=header)
        selector = Selector(text=response.text)
        all_trs = selector.css('#ip_list tr')
        ip_list = []
        for tr in all_trs[1:]:
            speed_str = tr.css('.bar::attr(title)').extract_first()
            if speed_str:
                speed = float(speed_str.split('秒')[0])
            all_texts = tr.css('td::text').extract()
            ip = all_texts[0]
            port = all_texts[1]
            proxy_type = all_texts[5]
            ip_list.append((ip, port, speed, proxy_type))
        for ip in ip_list:
            print(ip)
            cursor.execute(
                """
                insert ip_list(ip,port,speed,proxy_type) values('{0}','{1}',{2},'{3}') ON DUPLICATE KEY 
                UPDATE ip=VALUES(ip), port=VALUES(port), speed=VALUES(speed), proxy_type=VALUES(proxy_type)
                """.format(ip[0], ip[1], ip[2], ip[3])
            )
            conn.commit()


class GetIP(object):
    def delete_ip(self, ip):
        delete_sql = """
        delete frome ip_list where ip='{0}'
        """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port, proxy_type):
        # 判断ip是否可用
        http_url = 'http://www.baidu.com'
        proxy_url = '{0}://{1}:{2}'.format(proxy_type, ip, port)
        try:
            proxy_dict = {
                proxy_type:proxy_url
            }
            response = requests.get(http_url, proxies=proxy_dict)
            return True
        except Exception as e:
            print('invalid ip and port')
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print('effective ip')
                return True
            else:
                print('invalid ip and port')
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        # 从数据库中随机获取一个可用ip
        random_sql = """
        SELECT ip, port, proxy_type FROM ip_list
        ORDER BY RAND()
        LIMIT 1
        """
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            proxy_type = ip_info[2]
            judge_re = self.judge_ip(ip, port, proxy_type)
            if judge_re:
                return '{0}://{1}:{2}'.format(proxy_type.lower(), ip, port)
            else:
                return self.get_random_ip()


if __name__ == '__main__':
    ip = GetIP()
    print(ip.get_random_ip())

