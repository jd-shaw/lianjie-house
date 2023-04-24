import requests
from bs4 import BeautifulSoup
import re
import time
import openpyxl


# 抓取各个区域下二手房的页面
def get_page_url():
    # 定义空列表，用于创建所有的爬虫链接
    urls = []
    # 指定爬虫所需的南京各个区域名称
    #     regions = ['jiangning','qinhuai','gulou','jianye','xuanwu','yuhuatai','qixia','pukou']
    regions = ['jiangning']  # 测试，只抓取江宁区的
    for i in regions:
        url = 'https://nj.lianjia.com/xiaoqu/%s/' % i
        headers = {'User-Agent':
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
        res = requests.get(url, headers=headers)  # 发送get请求
        res = res.text.encode(res.encoding).decode('utf-8')  # 需要转码，否则可能会有问题
        soup = BeautifulSoup(res, 'html.parser')  # 对响应的链接源代码进行html解析
        page = soup.findAll('div', {'class': 'page-box house-lst-page-box'})  # 获取指定标签和属性下的内容
        pages = int(re.compile('\d+').findall(page[0]['page-data'])[0])
        # for j in list(range(1, pages + 1)): # 拼接所有需要爬虫的链接,如果都要把下面的代码替换成这句
        for j in list(range(1, 2)):  # 拼接所有需要爬虫的链接,测试只跑几页
            page_url = 'https://nj.lianjia.com/xiaoqu/%s/pg%d/' % (i, j)
            urls.append(page_url)
            print('目前爬取完{}，爬取了{}页面,爬取的页面URL是{}'.format(i, j, page_url))
        time.sleep(3)
    return urls


# 抓取各个区域下二手房的页面
def get_page_url2():
    # 定义空列表，用于创建所有的爬虫链接
    urls = []
    url = 'https://nj.lianjia.com/xiaoqu/jiangning/y3/'
    headers = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
    res = requests.get(url, headers=headers)  # 发送get请求
    res = res.text.encode(res.encoding).decode('utf-8')  # 需要转码，否则可能会有问题
    soup = BeautifulSoup(res, 'html.parser')  # 对响应的链接源代码进行html解析
    page = soup.findAll('div', {'class': 'page-box house-lst-page-box'})  # 获取指定标签和属性下的内容
    pages = int(re.compile('\d+').findall(page[0]['page-data'])[0])
    # for j in list(range(1, pages + 1)): # 拼接所有需要爬虫的链接,如果都要把下面的代码替换成这句
    for j in list(range(1, pages + 1)):  # 拼接所有需要爬虫的链接,测试只跑几页
        page_url = 'https://nj.lianjia.com/xiaoqu/jiangning/pg%dy3/' % j
        urls.append(page_url)
        print('爬取了{}页面,爬取的页面URL是{}'.format(j, page_url))
    time.sleep(3)
    return urls


def get_url_response(url):
    try:
        headers = {'User-Agent':
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
        res = requests.get(url, headers=headers)  # 发送get请求
        res = res.text.encode(res.encoding).decode('utf-8')
        soup = BeautifulSoup(res, 'html.parser')  # 对响应的链接源代码进行html解析
        return soup
    except Exception as err:
        pass


# 抓取具体二手房的URL
def get_house_url(url_list):
    data = [("区域", "价格", "年限", "名称", "链接")]
    i = 0
    for url in url_list:
        try:
            headers = {'User-Agent':
                           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
            res = requests.get(url, headers=headers)  # 发送get请求
            res = res.text.encode(res.encoding).decode('utf-8')
            soup = BeautifulSoup(res, 'html.parser')  # 对响应的链接源代码进行html解析
            # soup1 = soup.findAll('div',{'class':'title'})
            infos = soup.select('.xiaoquListItem')  # 爬取每页二手房下详细二手房的URL,每页二手房下有30个
            for i in range(0, len(infos) - 1):
                info = infos[i]
                name = info.select(".title a")[0].text
                soldNumber = info.select(".houseInfo a")[0].text
                rent = info.select(".houseInfo a")[1].text
                area = info.select(".positionInfo a")[0].text
                area1 = info.select(".positionInfo a")[1].text
                avgPrice = info.select(".xiaoquListItemPrice span")[0].text
                soldCount = info.select(".xiaoquListItemSellCount span")[0].text

                innerSoup = get_url_response(info.select(".title a")[0]['href'])
                place = innerSoup.select(".detailDesc")[0].text
                focusOn = innerSoup.select(".detailFollowedNum span")[0].text
                buildTime = innerSoup.select(".xiaoquInfoItem span")[0].text
                buildTime1 = innerSoup.select(".xiaoquInfoItem span")[1].text

                type = innerSoup.select(".xiaoquInfoItem span")[2].text
                type1 = innerSoup.select(".xiaoquInfoItem span")[3].text

                fee = innerSoup.select(".xiaoquInfoItem span")[4].text
                fee1 = innerSoup.select(".xiaoquInfoItem span")[5].text

                buildCompany = innerSoup.select(".xiaoquInfoItem span")[6].text
                buildCompany1 = innerSoup.select(".xiaoquInfoItem span")[7].text

                buildBy = innerSoup.select(".xiaoquInfoItem span")[8].text
                buildBy1 = innerSoup.select(".xiaoquInfoItem span")[9].text

                buildCount = innerSoup.select(".xiaoquInfoItem span")[10].text
                buildCount1 = innerSoup.select(".xiaoquInfoItem span")[11].text

                # 最近成交记录
                sold1 = []
                for li in innerSoup.select(".frameDealListItem li"):
                    sold2 = []
                    for div in li.select("div"):
                        if div.text not in sold2:
                            sold2.append(div.text)
                    sold1.append("\t".join(sold2))

                tmp = "\n".join((buildTime + ":" + buildTime1, type + ":" + type1, type + ":" + type1, fee + ":" + fee1,
                                 buildCompany + ":" + buildCompany1, buildBy + ":" + buildBy1,
                                 buildCount + ":" + buildCount1))
                tmpSold = "\n".join(sold1)
                print('爬取第{}/{}条信息'.format(i, len(url_list)))
                i = i + 1
                print(','.join(
                    (name, area, area1, avgPrice, "", "", "", place, soldNumber, rent, soldCount, focusOn, tmp)))
                data.append((name, area, area1, avgPrice, "", "", "", place, soldNumber, rent, soldCount, focusOn, tmp,
                             tmpSold, url))

            time.sleep(3)
        except Exception as err:
            pass

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    for row_index, row_data in enumerate(data, start=1):
        for col_index, cell_value in enumerate(row_data, start=1):
            # 获取单元格对象并更新值
            cell = sheet.cell(row=row_index, column=col_index)
            cell.value = cell_value
    workbook.save(filename='community_data2.xlsx')
    # 关闭Excel文件
    workbook.close()
    print('抓取完毕！')


if __name__ == '__main__':
    page_urls = get_page_url2()
    get_house_url(page_urls)
