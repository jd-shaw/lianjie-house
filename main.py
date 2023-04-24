import requests
from bs4 import BeautifulSoup
import re
import xlrd
import xlwt
import xlutils.copy
import time

def GetHTML(Url):
    """
    1、通过传入url组合，获取所有网页地址的url
    2、获取目标网页的html代码并进行解析
    3、解析后将目标信息分别写入字典类型的变量并返回

    @param Url: 目标网址的不变链接
    @return: 网站目标信息

    """

    #通过传入url组合，获取所有网页地址的url
    WebDiZhi = []
    for i in range(1,5):
        UrlHTML = Url + str(i)
        WebDiZhi.append(UrlHTML)

    print("共计{}页".format(len(WebDiZhi)))
    # Create_File()
    #获取目标网页的html代码并进行解析
    Xu = 0
    Shuliang = len(WebDiZhi)
    while Xu in range(Shuliang):#range(len(WebDiZhi))--循环整个列表

        Web = requests.get(WebDiZhi[Xu])
        WebText = Web.text

        #第一步、粗筛选目标信息所在的html代码，去除大部分无效信息代码
        soup_One = BeautifulSoup(WebText,'html.parser')
        XinXi_One = soup_One.find_all(class_="resblock-list-wrapper")

        #第二步、进一步筛选目标信息所在html代码，去除无效信息代码
        soup_Two = BeautifulSoup(str(XinXi_One),'lxml')
        XinXi_Two = soup_Two.find_all(class_="resblock-desc-wrapper")

        print("-----------------第{}页爬取成功------------".format(Xu))
    #     Html.append(XinXi_Two)
    #     time.sleep(1)
    # return Html

        print("-----------------开始写入第{}页-------------".format(Xu))
        Name = GetName(XinXi_Two)  # 获取小区名称
        Write_File(Name, 0,Xu)
        print("---------小区名称写入成功---------")
        time.sleep(3)
        Nature = NatureHouse(XinXi_Two)  # 获取小区住宅性质（住宅、商业性）
        Write_File(Nature, 1,Xu)
        print("---------小区性质写入成功---------")
        time.sleep(3)
        Status = StatusHouse(XinXi_Two)  # 获取小区状态（在售）
        Write_File(Status, 2,Xu)
        print("---------小区状态写入成功---------")
        time.sleep(3)
        Address = AddressHouse(XinXi_Two)  # 获取小区地址
        Write_File(Address, 3,Xu)
        print("---------小区地址写入成功---------")
        time.sleep(3)
        Area = AreaHouse(XinXi_Two)  # 获取小区房屋面积
        Write_File(Area, 4,Xu)
        print("---------小区面积写入成功---------")
        time.sleep(3)
        Average = AveragePriceHouse(XinXi_Two)  # 均价
        Write_File(Average, 5,Xu)
        print("---------小区均价写入成功---------")
        time.sleep(3)
        Total = TotalPriceHouse(XinXi_Two)  # 总价
        Write_File(Total, 6,Xu)
        print("---------小区总价写入成功---------")
        time.sleep(3)

        Xu += 1

        # 调用不同函数获取不同信息


def Write_File(Data, lei,Hang):
    data = xlrd.open_workbook(r"F:\实例\Python实例\爬虫\111.xls")
    ws = xlutils.copy.copy(data)
    table = ws.get_sheet(0)
    Shu = Hang * 10
    for i in range(len(Data)):
        table.write(i + 1 + Shu, lei, Data[i])
        print("----第{}项写入成功----".format(i))
        ws.save(r"F:\实例\Python实例\爬虫\111.xls")


def GetName(XinXi):
    """
    @param XinXi: 传入GetHTML函数第二步中筛选出的div标签下的html代码以及目标信息
    @return: 返回小区名称，列表类型
    """
    Nmae_list = []
    # 获取小区名称
    Obtain_Name_One = BeautifulSoup(str(XinXi), 'lxml')
    Name_One = Obtain_Name_One.findAll(class_="name")
    for i in Name_One:
        Get_A = BeautifulSoup(str(i), 'lxml')
        Nmae_list.append(Get_A.string)
    return Nmae_list

"""
代码以及目标信息均已获取，通过不同函数将html代码在对应函数中逐一进行解析获取函数对应信息并保存即可
以下为部分函数，其他函数未定义

"""
def NatureHouse(Nature):
    """房屋性质"""
    Nature_list = []
    Obtain_Nature = BeautifulSoup(str(Nature), 'lxml')
    Nature_one = Obtain_Nature.find_all(class_='resblock-type')
    for i in Nature_one:
        Get_Span = BeautifulSoup(str(i), 'lxml')
        Nature_list.append(Get_Span.string)
    return Nature_list

def StatusHouse(Status):
    """房屋状态"""
    Status_list = []
    Obtain_Nature = BeautifulSoup(str(Status), 'lxml')
    Status_one = Obtain_Nature.find_all(class_='sale-status')
    for i in Status_one:
        Get_Span = BeautifulSoup(str(i), 'lxml')
        Status_list.append(Get_Span.string)
    return Status_list

def AddressHouse(Area):
    """


    @param Area:传入GetHTML函数第二步中筛选出的div标签下的html代码以及目标信息
    @return:
    Analysis_Label_xxx:分析标签，xxx：代表第几次分析
    Target_Information_xxx:目标信息，xxx：代表第几个信息部分，总共分为两部分，以及一个整体信息存储列表Target_Information_list
    """
    #获取标签
    Target_Information_list = []
    Analysis_Label_One = BeautifulSoup(str(Area), 'lxml')
    # 获取div标签，calss=resblock-location
    Get_label_One = Analysis_Label_One.find_all(class_='resblock-location')
    #解析标签并获得span标签
    Analysis_Label_Two = BeautifulSoup(str(Get_label_One), 'lxml')
    Get_label_Two = Analysis_Label_Two.find_all(name='span')


    #获取span标签里面的文字内容并保存在列表内

    #第一个
    Target_Information_One = []
    for i in Get_label_Two:
        #使用正则表达式取出内部信息并保存在列表中
        Information_Str = re.sub(r'<.*?>','',str(i))
        Target_Information_One.append(Information_Str)
    #将列表内相同小区的地址进行合并，使用循环嵌套获取内容、合并最后保存在列表内
    i = 1
    a = 0

    #第二个，第二个信息是在第一个信息的基础上合并列表内的元素得来
    Target_Information_Two = []
    while i <= len(Target_Information_One):
        while a < i:
            #将Target_Information_One中每两项进行合并
            Information_Two = Target_Information_One[a]
            Information_One = Target_Information_One[i]
            Information_Three = Information_One + Information_Two

            Target_Information_Two.append(Information_Three)
            a += 2
        i += 2


    #获取详细地址

    #第三个
    Target_Information_Three = []
    Span_html_One = Analysis_Label_Two.find_all(name='a')
    for c in Span_html_One:
        Area_Str_1 = re.sub(r'<.*?>', '', str(c))
        Target_Information_Three.append(Area_Str_1)


    # 将Target_Information_Two和Target_Information_Three两个列表中的各项元素分别进行合并并保存在Area_list列表中
    A = min(len(Target_Information_Two),len(Target_Information_Three))
    for i in range(A):
        Target_Information_list.append(Target_Information_Two[i] + Target_Information_Three[i])


    return Target_Information_list


def AreaHouse(Area):
    """

    @param Area: 传入GetHTML函数第二步中筛选出的div标签下的html代码以及目标信息
    @return: 返回房屋房间数量以及房屋总面积
    """
    Area_list = []
    #筛选目标信息的父标签
    Obtain_Area_One = BeautifulSoup(str(Area), 'lxml')
    Area_one = Obtain_Area_One.find_all(class_='resblock-room')

    #通过正则表达式去除多余的html标签信息
    Get_Area_One = []
    for c in Area_one:
        Area_Str_1 = re.sub(r'<.*?>', '', str(c))
        Get_Area_One.append(Area_Str_1)

    #通过正则表达式去除多余的换行符
    Get_Area_Two = []
    for i in Get_Area_One:
        Area_Str_2 = re.sub(r'\s+','',str(i))
        Get_Area_Two.append(Area_Str_2)


    #开始获取房屋总面积
    Obtain_Area_Two = BeautifulSoup(str(Area),'lxml')
    Area_two = Obtain_Area_Two.find_all(class_='resblock-area')
    #通过正则表达式去除多余的html标签信息
    Get_Area_Three = []
    for a in Area_two:
        Area_Str_3 = re.sub(r'<.*?>', '', str(a))
        Get_Area_Three.append(Area_Str_3)

    # 通过正则表达式去除多余的换行符
    Get_Area_Four = []
    for r in Get_Area_Three:
        Area_Str_4 = re.sub(r'\s+', '', str(r))
        Get_Area_Four.append(Area_Str_4)

    # 将Get_Area_Two和Get_Area_Four两个列表中的各项元素分别进行合并并保存在Area_list列表中
    A = min(len(Get_Area_Two), len(Get_Area_Four))
    for i in range(A):
        Area_list.append(Get_Area_Two[i] + Get_Area_Four[i])

    return Area_list

def AveragePriceHouse(Average):
    """
    房屋均价
    @param Average:
    @return:
    """
    Average_list = []
    Obtain_Average = BeautifulSoup(str(Average), 'lxml')
    Average_one = Obtain_Average.find_all(class_='number')
    for i in Average_one:
        Get_Span = BeautifulSoup(str(i), 'lxml')
        Average_list.append(Get_Span.string)

    return Average_list



def TotalPriceHouse(Total):
    """
    房屋总价

    @param Total:
    @return:
    """
    Total_list = []
    Obtain_Total = BeautifulSoup(str(Total), 'lxml')
    Total_one = Obtain_Total.fjind_all(class_='second')
    for i in Total_one:
        Get_Span = BeautifulSoup(str(i), 'lxml')
        Get_Span_one = Get_Span.string
        Get_Span_two = Get_Span_one.lstrip('总价')
        Total_list.append(Get_Span_two)


    return Total_list


def Create_File():
    name = ['名称','性质','状态','地址','面积','均价','总价',]
    workbook = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = workbook.add_sheet('shett1', cell_overwrite_ok=True)
    for i in range(len(name)):
        sheet.write(0, i, name[i])
    workbook.save('/Users/xiaojindong/Downloads/111.xlsx')
    print("文件创建成功")


if __name__ == '__main__':
    url = "https://nj.lianjia.com/ershoufang/pg"
    Create_File()
    DataHtml = GetHTML(url)

    print("全部房产信息写入成功")