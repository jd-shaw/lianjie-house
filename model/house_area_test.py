import requests
from bs4 import BeautifulSoup

from model.House import House


def get_house_message(url2):
    with open('lianjia-2023-04-12-03.csv', 'w', encoding='utf-8') as f:
        f.write(','.join(("region", "price", "year", "name", "subway", "ype", "floor", "area", "decorationSituation",
                          "elevators", "tructure", "innerArea", "buildType", "toward", "buildStructure", "uploadTime",
                          "transactionOwnership", "lastTransaction", "use", "useLimit", "ownership", "mortgageInfo",
                          "roombook")) + '\n')
        i = 0
        for url in url2:
            try:
                house = House()
                headers = {'User-Agent':
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
                res = requests.get(url, headers=headers)  # 发送get请求
                res = res.text.encode(res.encoding).decode('utf-8')  # 需要转码，否则会有问题
                soup = BeautifulSoup(res, 'html.parser')  # 使用bs4模块，对响应的链接源代码进行html解析
                house.region = soup.select('.areaName .info')[0].text
                house.price = soup.select('.price span')[0].text  # 抓取页面内容
                house.year = soup.select('.subInfo')[2].text
                house.name = soup.select('.aroundInfo a')[0].text
                house.subway = soup.select('.areaName .supplement')[0]['title']

                # 基本信息
                house.houseType = soup.select('.base .content li')[0].text[4:]
                house.floor = soup.select('.base .content li')[1].text[4:]
                house.area = soup.select('.base .content li')[2].text[4:]
                house.houseStructure = soup.select('.base .content li')[3].text[4:]
                house.innerArea = soup.select('.base .content li')[4].text[4:]
                house.buildType = soup.select('.base .content li')[5].text[4:]
                house.toward = soup.select('.base .content li')[6].text[4:]
                house.buildStructure = soup.select('.base .content li')[7].text[4:]
                house.decorationSituation = soup.select('.base .content li')[8].text[4:]
                house.ladderRatio = soup.select('.base .content li')[9].text[4:]
                house.elevators = soup.select('.base .content li')[10].text[4:]

                for index, transaction in enumerate(soup.select('.transaction .content span')):

                    if transaction.text == "挂牌时间":
                        house.uploadTime = soup.select('.transaction .content span')[index + 1].text
                    if transaction.text == "交易权属":
                        house.transactionOwnership = soup.select('.transaction .content span')[index + 1].text
                    if transaction.text == "上次交易":
                        house.lastTransaction = soup.select('.transaction .content span')[index + 1].text
                    if transaction.text == "房屋用途":
                        house.use = soup.select('.transaction .content span')[index + 1].text
                    if transaction.text == "房屋年限":
                        house.useLimit = soup.select('.transaction .content span')[index + 1].text
                    if transaction.text == "产权所属":
                        house.ownership = soup.select('.transaction .content span')[index + 1].text
                    # if transaction.text == "抵押信息":
                    #     house.mortgageInfo = soup.select('.transaction .content span')[index + 1].text
                    # if transaction.text == "房本备件":
                    #     house.roombook = soup.select('.transaction .content span')[index + 1].text
                print('爬取第{}条信息'.format(i))
                i = i + 1
                data = (house.region, house.price, house.year, house.name, house.subway, house.houseType,
                        house.floor, house.area, house.decorationSituation, house.elevators,
                        house.houseStructure, house.innerArea, house.buildType, house.toward,
                        house.buildStructure, house.uploadTime, house.transactionOwnership,
                        house.lastTransaction, house.use, house.useLimit, house.ownership, house.mortgageInfo,
                        house.roombook)
                print(','.join(data))
                f.write(','.join(data) + '\n')
            except Exception as err:
                pass
    print('抓取完毕！')


if __name__ == '__main__':
    house_urls = ["https://nj.lianjia.com/ershoufang/103124821277.html"]
    get_house_message(house_urls)
