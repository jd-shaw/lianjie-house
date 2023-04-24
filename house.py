import requests
from bs4 import BeautifulSoup
import re
import time


# 抓取各个区域下二手房的页面
def get_page_url():
    # 定义空列表，用于创建所有的爬虫链接
    urls = []
    # 指定爬虫所需的南京各个区域名称
    #     regions = ['gulou','jianye','qinhuai','xuanwu','yuhuatai','qixia','jiangning','pukou']
    regions = ['jiangning']
    # 基于for循环，构造完整的爬虫链接
    for i in regions:
        url = 'http://nj.lianjia.com/ershoufang/%s/' % i
        headers = {'User-Agent':
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
        res = requests.get(url, headers=headers)  # 发送get请求
        res = res.text.encode(res.encoding).decode('utf-8')  # 需要转码，否则会有问题
        soup = BeautifulSoup(res, 'html.parser')  # 使用bs4模块，对响应的链接源代码进行html解析
        page = soup.findAll('div', {'class': 'page-box house-lst-page-box'})  # 使用finalAll方法，获取指定标签和属性下的内容
        pages = int(re.compile('\d+').findall(page[0]['page-data'])[0])
        for j in list(range(1, pages + 1)):  # 拼接所有需要爬虫的链接
            page_url = 'http://nj.lianjia.com/ershoufang/%s/pg%d/' % (i, j)
            urls.append(page_url)
            print('目前爬取完{}，爬取了{}页面,爬取的页面URL是{}'.format(i, j, page_url))
        time.sleep(3)
    return urls


# 抓取具体二手房的URL
def get_house_url(url_list):
    url2 = []
    for url in url_list:
        try:
            headers = {'User-Agent':
                           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
            res = requests.get(url, headers=headers)  # 发送get请求
            res = res.text.encode(res.encoding).decode('utf-8')  # 需要转码，否则会有问题
            soup = BeautifulSoup(res, 'html.parser')  # 使用bs4模块，对响应的链接源代码进行html解析
            # soup1 = soup.findAll('div',{'class':'title'})
            soup1 = soup.select('.title a')  # 爬取每页二手房下详细二手房的URL,每页二手房下有30个二手房详细信息URL
            for i in range(0, len(soup1) - 1):
                url2.append(soup1[i]['href'])
                print('爬取{}页面下，第{}条房源URL:{}'.format(url, i, soup1[i]['href']))
            time.sleep(3)
        except Exception as err:
            pass
    return url2


def get_house_message(url2):
    with open('lianjia-qxjnpk.csv', 'w', encoding='utf-8') as f:
        i = 0
        for url in url2:
            try:
                headers = {'User-Agent':
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
                res = requests.get(url, headers=headers)  # 发送get请求
                res = res.text.encode(res.encoding).decode('utf-8')  # 需要转码，否则会有问题
                soup = BeautifulSoup(res, 'html.parser')  # 使用bs4模块，对响应的链接源代码进行html解析
                region = soup.select('.areaName .info')[0].text
                price = soup.select('.price span')[0].text  # 抓取页面内容
                year = soup.select('.subInfo')[2].text
                name = soup.select('.aroundInfo a')[0].text
                subway = soup.select('.areaName .supplement')[0]['title']
                housetype = soup.select('.base .content li')[0].text[4:]
                floor = soup.select('.base .content li')[1].text[4:]
                area = soup.select('.base .content li')[2].text[4:]
                Decoration_situation = soup.select('.base .content li')[8].text[4:]
                elevators = soup.select('.base .content li')[10].text[4:]
                # property_rights = soup.select('.base .content li')[11].text[4:]
                print('爬取第{}条信息'.format(i))
                i = i + 1
                print(','.join((region, price, year, name, subway, housetype, floor, area, Decoration_situation,
                                elevators)))
                f.write(','.join((region, price, year, name, subway, housetype, floor, area, Decoration_situation,
                                  elevators)) + '\n')
            except Exception as err:
                pass
    print('抓取完毕！')


if __name__ == '__main__':
    page_urls = get_page_url()
    house_urls = get_house_url(page_urls)
    get_house_message(house_urls)
