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
        url = 'http://nj.lianjia.com/ershoufang/%s/' % i
        headers = {'User-Agent':
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
        res = requests.get(url, headers=headers)  # 发送get请求
        res = res.text.encode(res.encoding).decode('utf-8')  # 需要转码，否则可能会有问题
        soup = BeautifulSoup(res, 'html.parser')  # 对响应的链接源代码进行html解析
        page = soup.findAll('div', {'class': 'page-box house-lst-page-box'})  # 获取指定标签和属性下的内容
        pages = int(re.compile('\d+').findall(page[0]['page-data'])[0])
        # for j in list(range(1, pages + 1)): # 拼接所有需要爬虫的链接,如果都要把下面的代码替换成这句
        for j in list(range(1, 3)):  # 拼接所有需要爬虫的链接,测试只跑几页
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
            res = res.text.encode(res.encoding).decode('utf-8')
            soup = BeautifulSoup(res, 'html.parser')  # 对响应的链接源代码进行html解析
            # soup1 = soup.findAll('div',{'class':'title'})
            soup1 = soup.select('.title a')  # 爬取每页二手房下详细二手房的URL,每页二手房下有30个
            for i in range(0, len(soup1) - 1):
                url2.append(soup1[i]['href'])
                print('共计：{},爬取{}页面下，第{}条房源URL:{}'.format(len(url2), url, i, soup1[i]['href']))
            time.sleep(3)
        except Exception as err:
            pass
    return url2


# 抓取某个区域、小区的URL
def get_house_area(url_list):
    area_urls = []
    # 指定爬虫所需的南京各个区域名称
    for i, url in enumerate(url_list):
        headers = {'User-Agent':
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
        res = requests.get(url, headers=headers)  # 发送get请求
        res = res.text.encode(res.encoding).decode('utf-8')
        soup = BeautifulSoup(res, 'html.parser')
        page = soup.findAll('div', {'class': 'page-box house-lst-page-box'})  # 获取指定标签和属性下的内容
        pages = int(re.compile('\d+').findall(page[0]['page-data'])[0])
        for j in list(range(1, pages + 1)):  # 拼接所有需要爬虫的链接
            # https://nj.lianjia.com/ershoufang/pg3c1411063827536/
            # https://nj.lianjia.com/ershoufang/c1411063827536/
            # https://nj.lianjia.com/ershoufang/qixia/pg2ie1f1f2l3p5/  条件：栖霞 、三室、朝南、朝东、无电梯、200-300
            # 上面的链接就把 ershoufang/pg%s 换成 ershoufang/qixia/pg%s
            page_url = url.replace("ershoufang/", "ershoufang/pg%s" % j)
            area_urls.append(page_url)
            print('目前爬取完{}，爬取了{}页面,爬取的页面URL是{}'.format(i, j, page_url))
        time.sleep(3)
    return area_urls


# 导出csv格式的文件
def get_house_message(url2):
    with open('lianjia-2023-04-12-2.csv', 'w', encoding='utf-8') as f:
        f.write(','.join(
            ("区域", "价格", "年限", "名称", "地铁", "房屋类型", "所在楼层", "建筑面积", "户型结构", "套内面积", "建筑类型", "房屋朝向", "建筑结构", "装修情况",
             "梯户比例", "配备电梯", "挂牌时间", "交易权属", "上次交易", "房屋用途", "房屋年限", "产权所属", "链接")) + '\n')
        i = 0
        for url in url2:
            try:
                headers = {'User-Agent':
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
                res = requests.get(url, headers=headers)  # 发送get请求
                res = res.text.encode(res.encoding).decode('utf-8')  # 需要转码，否则会有问题
                soup = BeautifulSoup(res, 'html.parser')  # 对响应的链接源代码进行html解析
                region = soup.select('.areaName .info')[0].text
                price = soup.select('.price span')[0].text  # 抓取页面内容
                year = soup.select('.subInfo')[2].text
                name = soup.select('.aroundInfo a')[0].text
                subway = soup.select('.areaName .supplement')[0]['title']

                # 基本信息
                houseType = soup.select('.base .content li')[0].text[4:]
                floor = soup.select('.base .content li')[1].text[4:]
                area = soup.select('.base .content li')[2].text[4:]
                tructure = soup.select('.base .content li')[3].text[4:]
                innerArea = soup.select('.base .content li')[4].text[4:]
                buildType = soup.select('.base .content li')[5].text[4:]
                toward = soup.select('.base .content li')[6].text[4:]
                buildStructure = soup.select('.base .content li')[7].text[4:]
                decorationSituation = soup.select('.base .content li')[8].text[4:]
                ladderRatio = soup.select('.base .content li')[9].text[4:]
                elevators = soup.select('.base .content li')[10].text[4:]

                uploadTime = ""
                transactionOwnership = ""
                lastTransaction = ""
                use = ""
                useLimit = ""
                ownership = ""
                for index, transaction in enumerate(soup.select('.transaction .content span')):
                    if transaction.text == "挂牌时间":
                        uploadTime = soup.select('.transaction .content span')[index + 1].text
                    if transaction.text == "交易权属":
                        transactionOwnership = soup.select('.transaction .content span')[index + 1].text
                    if transaction.text == "上次交易":
                        lastTransaction = soup.select('.transaction .content span')[index + 1].text
                    if transaction.text == "房屋用途":
                        use = soup.select('.transaction .content span')[index + 1].text
                    if transaction.text == "房屋年限":
                        useLimit = soup.select('.transaction .content span')[index + 1].text
                    if transaction.text == "产权所属":
                        ownership = soup.select('.transaction .content span')[index + 1].text

                print('爬取第{}条信息'.format(i))
                i = i + 1
                print(','.join((region, price, year, name, subway, houseType, floor, area, tructure, innerArea,
                                buildType, toward, buildStructure, decorationSituation,
                                ladderRatio, elevators, uploadTime, transactionOwnership, lastTransaction, use,
                                useLimit, ownership)))  # 打印信息

                f.write(','.join((region, price, year, name, subway, houseType, floor, area, tructure, innerArea,
                                  buildType, toward, buildStructure, decorationSituation,
                                  ladderRatio, elevators, uploadTime, transactionOwnership, lastTransaction, use,
                                  useLimit, ownership, url)) + '\n')
                time.sleep(3)
            except Exception as err:
                pass
    print('抓取完毕！')


# 导出Excel表格
def get_house_message_excel(url2):
    data = [("区域", "价格", "年限", "名称", "地铁", "房屋类型", "所在楼层", "建筑面积", "户型结构", "套内面积", "建筑类型", "房屋朝向", "建筑结构", "装修情况",
             "梯户比例", "配备电梯", "挂牌时间", "交易权属", "上次交易", "房屋用途", "房屋年限", "产权所属", "链接")]
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

            # 基本信息
            houseType = soup.select('.base .content li')[0].text[4:]
            floor = soup.select('.base .content li')[1].text[4:]
            area = soup.select('.base .content li')[2].text[4:]
            tructure = soup.select('.base .content li')[3].text[4:]
            innerArea = soup.select('.base .content li')[4].text[4:]
            buildType = soup.select('.base .content li')[5].text[4:]
            toward = soup.select('.base .content li')[6].text[4:]
            buildStructure = soup.select('.base .content li')[7].text[4:]
            decorationSituation = soup.select('.base .content li')[8].text[4:]
            ladderRatio = soup.select('.base .content li')[9].text[4:]
            elevators = soup.select('.base .content li')[10].text[4:]

            uploadTime = ""
            transactionOwnership = ""
            lastTransaction = ""
            use = ""
            useLimit = ""
            ownership = ""
            for index, transaction in enumerate(soup.select('.transaction .content span')):
                if transaction.text == "挂牌时间":
                    uploadTime = soup.select('.transaction .content span')[index + 1].text
                if transaction.text == "交易权属":
                    transactionOwnership = soup.select('.transaction .content span')[index + 1].text
                if transaction.text == "上次交易":
                    lastTransaction = soup.select('.transaction .content span')[index + 1].text
                if transaction.text == "房屋用途":
                    use = soup.select('.transaction .content span')[index + 1].text
                if transaction.text == "房屋年限":
                    useLimit = soup.select('.transaction .content span')[index + 1].text
                if transaction.text == "产权所属":
                    ownership = soup.select('.transaction .content span')[index + 1].text

            print('爬取第{}条信息'.format(i))
            i = i + 1
            print(','.join((region, price, year, name, subway, houseType, floor, area, tructure, innerArea,
                            buildType, toward, buildStructure, decorationSituation,
                            ladderRatio, elevators, uploadTime, transactionOwnership, lastTransaction, use,
                            useLimit, ownership)))
            data.append((region, price, year, name, subway, houseType, floor, area, tructure, innerArea,
                         buildType, toward, buildStructure, decorationSituation,
                         ladderRatio, elevators, uploadTime, transactionOwnership, lastTransaction, use,
                         useLimit, ownership, url))
            time.sleep(5)
        except Exception as err:
            pass

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    for row_index, row_data in enumerate(data, start=1):
        for col_index, cell_value in enumerate(row_data, start=1):
            # 获取单元格对象并更新值
            cell = sheet.cell(row=row_index, column=col_index)
            cell.value = cell_value
    workbook.save(filename='example_data.xlsx')
    # 关闭Excel文件
    workbook.close()
    print('抓取完毕！')


if __name__ == '__main__':
    page_urls = get_house_area(["https://nj.lianjia.com/ershoufang/c1411063827536/"])
    # page_urls = get_page_url()
    house_urls = get_house_url(page_urls)
    get_house_message_excel(house_urls)
