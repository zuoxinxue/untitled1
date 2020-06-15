from icalendar import Calendar
import csv
from mysql_tool import Mysql_tool

import requests
from bs4 import BeautifulSoup
import re
import datetime


mysql_tool = Mysql_tool()
s = mysql_tool.connect()
"""
1 读取ATM


 2 读取来自谷歌日历的ics

 3 将duration处理成hour
"""

#正则处理部分
#匹配数字
#匹配时间格式前的数字 ，将duration上的时间段转化为分钟
def re_num_h(re_content_num):
    #re_content_num='02:30'
    regex_num = re.compile('\d+')
    re_num = regex_num.findall(re_content_num)
    #print(re_num)
    h_m = int(re_num[0])*60 + int(re_num[1])
    #print(h_m)
    return h_m

#匹配日期
def re_real_date(re_content_num):
    #print(re_content_num)
    re_content_num = '2020-05-11 17:43'
    regex_num = re.compile('\d+')
    re_num = regex_num.findall(re_content_num)
    print(re_num)
    #re_date = ''.join(re_num[2:5])
    real_today = ''.join(re_num[0:3])
    return real_today


# 1 从mysql中读取数据duration , 更新原数据库     【项目，时间，换算分钟，算了该项目占一天中的比例】
# 2 从原数据库再次取出，生成表格


# portion_time是用来处理atm中time_record的信息
def portion_time():

    # 查找信息 。该部分为查找的样例，后续需要增加功能 ，可以修改部分代码
    # 访部分传参需要注意，table_name是必须要输入的，其他 两个则可以为为空，区别就是实现的功能不一样
    # 该部分除如果传入表名，就是查找该表中的全部内容 ，
    """
    table_name = 'time_record'
    # 如果输入find_field，则为查找对应的字段
    find_field = 'classification,classification_v1,project,son_project,today,from_v1,to_v1,duration'
    # 如果办公设备查询条件，则是按条件查询
    # ?   该处取出的语句如何更智能化，？？？
    query_condition = "today like '2020_05_09' "
    """
    table_name = 'real_record'
    # 如果输入find_field，则为查找对应的字段
    find_field = 'summary,from_v1,to_v1'
    # 如果办公设备查询条件，则是按条件查询
    # ?   该处取出的语句如何更智能化，？？？
    query_condition = ""
    # 查询之后的数据进行一个处理程序
    result = mysql_tool.find_info(find_field, table_name, query_condition)
    print(result)
    # print(type(list(result)))

    #考虑用字典把他们放进去，字典好像有点问题
    #resutl_l = []
    resutl_ll = list(result)

    for result in resutl_ll:
        # print(result)
        result_list = list(result)
        print(result_list)
        result_project = result_list[7]
        time_num = result_list[7]
        #print(time_num)
        #print(type(time_num))
        #将时间段转化为分钟，再将分钟转化为小时，从而求百分比
        num_h = re_num_h(time_num)
        result_list[7]=num_h

        #使用mysql update 更新信息
        table_name = 'time_record'
        pro_change = "from_v1='{}'".format(result[5])
        post_change = "time_long='{}'".format(num_h)
        mysql_tool.update_info(table_name, post_change,pro_change)
        print(1)

# 计算两个日期时间之间的时间差
#  用于portion_real_ics
def minNums(startTime, endTime):
    '''计算两个时间点之间的分钟数'''
    # 处理格式,加上秒位
    #原始日期格式如下
    """
    startTime_1 = '2020-05-09 16:30:00'
    endTime_1 = '2020-05-10 01:45:00'
    """
    startTime1 = startTime
    endTime1 = endTime
    # 计算分钟数
    startTime2 = datetime.datetime.strptime(startTime1, "%Y-%m-%d %H:%M:%S")
    endTime2 = datetime.datetime.strptime(endTime1, "%Y-%m-%d %H:%M:%S")
    seconds = (endTime2 - startTime2).seconds
    # 来获取时间差中的秒数。注意，seconds获得的秒只是时间差中的小时、分钟和秒部分的和，并没有包含时间差的天数（既是两个时间点不是同一天，失效）
    total_seconds = (endTime2 - startTime2).total_seconds()
    # 来获取准确的时间差，并将时间差转换为秒
    print(total_seconds)
    mins = total_seconds / 60
    return int(mins)

#匹配日期
#用于portion_real_ics 中的日期
def re_today_ics(re_content_num):
    #print(re_content_num)
    #传入参数格式：
    #re_content_num = '2020-06-01 03:25:00+00:00'
    regex_num = re.compile('\d+')
    re_num = regex_num.findall(re_content_num)
    re_date = ''.join(re_num[0:3])
    print(re_date, 1)
    return re_date

def portion_real_ics():

    # 查找信息 。该部分为查找的样例，后续需要增加功能 ，可以修改部分代码
    # 访部分传参需要注意，table_name是必须要输入的，其他 两个则可以为为空，区别就是实现的功能不一样
    # 该部分除如果传入表名，就是查找该表中的全部内容 ，

    table_name = 'real_record'
    # 如果输入find_field，则为查找对应的字段
    find_field = 'summary,from_v1,to_v1'
    # 如果办公设备查询条件，则是按条件查询
    # ?   该处取出的语句如何更智能化，？？？
    query_condition = ""
    # 查询之后的数据进行一个处理程序
    result = mysql_tool.find_info(find_field, table_name, query_condition)
    print(result)
    # print(type(list(result)))

    #考虑用字典把他们放进去，字典好像有点问题
    #resutl_l = []
    resutl_ll = list(result)
    print(resutl_ll)
    for result in resutl_ll:
        print(result)
        result_list = list(result)
        print(result_list)
        from_v1 = result_list[1]
        com_from_v1 = from_v1
        re_today = re_today_ics(from_v1)
        from_v1 = from_v1.replace('+00:00','')
        to_v1 = result_list[2]
        to_v1 = to_v1.replace('+00:00', '')
        #两个时间差所减，得分钟数
        time_min = minNums(from_v1, to_v1)
        portion_allday = time_min*1000/(24*60)
        print(2,re_today,time_min)


        """
        #print(time_num)
        #print(type(time_num))
        #将时间段转化为分钟，再将分钟转化为小时，从而求百分比
        num_h = re_num_h(time_num)
        result_list[7]=num_h

        #使用mysql update 更新信息
        
        print(1)
        """
        table_name = 'real_record'
        pro_change = "from_v1='{}'".format(com_from_v1)
        post_change = "time_long='{}',today='{}',portion_allday='{}'".format(time_min,re_today,portion_allday)
        mysql_tool.update_info(table_name, post_change, pro_change)



# ics_real_record 对插进的同类进行加起一起
def sort_class():
    table_name = 'real_record'
    # 如果输入find_field，则为查找对应的字段
    find_field = 'summary,today,from_v1,time_long,portion_allday'
    # 如果办公设备查询条件，则是按条件查询
    # ?   该处取出的语句如何更智能化，？？？
    query_condition = "today like '20200528'"
    # 查询之后的数据进行一个处理程序
    result = mysql_tool.find_info(find_field, table_name, query_condition)
    print(result)
    # print(type(list(result)))

    # 考虑用字典把他们放进去，字典好像有点问题
    # resutl_l = []
    resutl_ll = list(result)
    print(resutl_ll)
    for result in resutl_ll:
        print(result)
        result_list = list(result)
        print(result_list)


        """
        from_v1 = result_list[1]
        com_from_v1 = from_v1
        re_today = re_today_ics(from_v1)
        from_v1 = from_v1.replace('+00:00', '')
        to_v1 = result_list[2]
        to_v1 = to_v1.replace('+00:00', '')
        # 两个时间差所减，得分钟数
        time_min = minNums(from_v1, to_v1)
        print(2, re_today, time_min)
        
        
        #print(time_num)
        #print(type(time_num))
        #将时间段转化为分钟，再将分钟转化为小时，从而求百分比
        num_h = re_num_h(time_num)
        result_list[7]=num_h

        #使用mysql update 更新信息

        print(1)
        
        table_name = 'real_record'
        pro_change = "from_v1='{}'".format(com_from_v1)
        post_change = "time_long='{}',today='{}'".format(time_min, re_today)
        mysql_tool.update_info(table_name, post_change, pro_change)

        """

portion_real_ics()

#portion_time()
sort_class()


