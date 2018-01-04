import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pandas as pd

user_agent = UserAgent()

url = 'http://hotel.elong.com/ajax/list/asyncsearch'


def generate_headers():
    headers = {
        'User-Agent': user_agent.random,
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Content-Length':'1602',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Host':'hotel.elong.com',
        'Origin':'http://hotel.elong.com',
        'Referer':'http://hotel.elong.com/beijing/',
        'X-Requested-With':'XMLHttpRequest'
    }
    return headers


def generate_formdata(page):
    formdata = {
        'code':'7605539',
        'listRequest.areaID':'',
        'listRequest.bookingChannel':'1',
        'listRequest.cardNo':'192928',
        'listRequest.checkInDate':'2018-01-05 00:00:00',
        'listRequest.checkOutDate':'2018-01-06 00:00:00',
        'listRequest.cityID':'0101',
        'listRequest.cityName':'北京市',
        'listRequest.customLevel':'11',
        'listRequest.distance':'20',
        'listRequest.endLat':'0',
        'listRequest.endLng':'0',
        'listRequest.facilityIds':'',
        'listRequest.highPrice':'0',
        'listRequest.hotelBrandIDs':'',
        'listRequest.isAdvanceSave':'false',
        'listRequest.isAfterCouponPrice':'true',
        'listRequest.isCoupon':'false',
        'listRequest.isDebug':'false',
        'listRequest.isLimitTime':'false',
        'listRequest.isLogin':'false',
        'listRequest.isMobileOnly':'true',
        'listRequest.isNeed5Discount':'true',
        'listRequest.isNeedNotContractedHotel':'false',
        'listRequest.isNeedSimilarPrice':'false',
        'listRequest.isReturnNoRoomHotel':'true',
        'listRequest.isStaySave':'false',
        'listRequest.isTrace':'false',
        'listRequest.isUnionSite':'false',
        'listRequest.keywords':'',
        'listRequest.keywordsType':'0',
        'listRequest.language':'cn',
        'listRequest.listType':'0',
        'listRequest.lowPrice':'0',
        'listRequest.orderFromID':'50794',
        'listRequest.pageIndex':str(page),
        'listRequest.pageSize':'20',
        'listRequest.payMethod':'0',
        'listRequest.personOfRoom':'0',
        'listRequest.poiId':'0',
        'listRequest.promotionChannelCod':'0000',
        'listRequest.proxyID':'ZD',
        'listRequest.rankType':'0',
        'listRequest.returnFilterItem':'true',
        'listRequest.sellChannel':'1',
        'listRequest.seoHotelStar':'0',
        'listRequest.sortDirection':'1',
        'listRequest.sortMethod':'1',
        'listRequest.starLevels':'',
        'listRequest.startLat':'0',
        'listRequest.startLng':'0',
        'listRequest.taRecommend':'false',
        'listRequest.themeIds':'',
        'listRequest.ctripToken':'96ab527a-edb0-4d99-9020-d551ec467248',
        'listRequest.elongToken':'jc0h7dj9-3147-483f-ac2e-8a564aee2df0'
    }
    return formdata


def generate_html(page):
    formdata = generate_formdata(str(page))
    headers = generate_headers()
    response = requests.post(url, data=formdata, headers=headers)
    html = response.json()['value']['hotelListHtml']
    return html


def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('.h_item')
    for item in items:
        yield (item.select('.h_info_b1 a')[0].get('title').strip(),
               item.select('.h_pri_num')[0].get_text().strip())

def main():
    hotels = []
    for i in range(1, 11):
        items = parse_html(generate_html(str(i)))
        for item in items:
            hotels.append(item)
            print(item)
    hotels = pd.DataFrame(hotels)
    hotels.to_csv('hotels.csv', header=False, index=False)

if __name__ == '__main__':
    main()