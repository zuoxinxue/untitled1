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
def re_num(self,re_content_num):
    regex_num = re.compile('\d+')
    re_num = regex_num.findall(re_content_num)

#匹配日期
def re_date(re_content_num):
    print(re_content_num)
    #re_content_num = '2020-05-11 17:43'
    regex_num = re.compile('\d+')
    re_num = regex_num.findall(re_content_num)
    re_date = ''.join(re_num[0:3])
    print(re_date, 1)
    return re_date


# 1 读取ATM

def read_html_local():

    path = 'D:\\study\\精力管理\\精力管理--图片\\精力管理\\思维\\时间管理\\时间记录表\\report-2020-5-20.html'
    #htmlfile = open(path, 'r', encoding='utf-8')

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        #print(content)
        soup = BeautifulSoup(content,'html.parser')
        #get_table = soup.table
        #print(get_table)
        #get_table.findall()
        get_table =soup.find_all('table')
        #print(get_table)
        n=0
        for table_v1 in get_table:

            table_shi_jian = table_v1.find_all('tr')

            #print(table_shi_jian)
            #print(table_v1)
            n += 1
            print(n)
            if n == 1:
                for project_shiJian in table_shi_jian:
                    #print(project_shiJian)
                    project = project_shiJian.find_all('td')
                    #print(project)
                    project_list=[]
                    for son in project:
                        #print(son)
                        son_project = son.text
                        #print(son_project)
                        project_list.append(son_project)
                    print(project_list)
                    if len(project_list) > 0:
                        regex_num = re.compile('\d+')
                        pro = project_list[0]
                        #print(pro)
                        classification = regex_num.findall(pro)
                        classification=int(classification[0])
                        classification_v1=project_list[0]
                        from_v1 = project_list[1]
                        today = re_date(from_v1)
                        print(today,2)
                        to_v1 = project_list[2]
                        duration = project_list[3]
                        #duration = float(duration)
                        date_num = datetime.date.today()
                        table_structure = 'time_record(num,classification,classification_v1,today,from_v1,to_v1,duration)'
                        values = "'{}','{}','{}','{}','{}','{}','{}'".format(date_num,classification,classification_v1,today,from_v1,to_v1,duration)
                        print(values)
                        mysql_tool.insert_info(table_structure, values)

            else:

                #比例这一块暂时还没有处理

                for project_shiJian in table_shi_jian:
                    # print(project_shiJian)
                    project = project_shiJian.find_all('td')
                    # print(project)
                    project_list = []
                    for son in project:
                        # print(son)
                        son_project = son.text
                        # print(son_project)
                        project_list.append(son_project)
                    # print(project_list)






# 2 读取来自谷歌日历的ics






headers = ('Summary', 'UID', 'Description', 'Location', 'Start Time', 'End Time', 'URL')

class CalendarEvent:
    """Calendar event class"""
    summary = ''
    uid = ''
    description = ''
    location = ''
    start = ''
    end = ''
    url = ''

    def __init__(self, name):
        self.name = name

events = []


#此处可以传入ics_path ,也可以批量导入
def read_ics():
    path = 'D:\\study\\自我管理\\zuoxinxue\\record_night_8f4u65s8k6grt8rtj72li3eq10.ics'
    # htmlfile = open(path, 'r', encoding='utf-8')

    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
        # print(data)
        gcal = Calendar.from_ical(data)
        #print(gcal)
        for component in gcal.walk():
            print(component.name)
            event = CalendarEvent("event")
            if component.get('SUMMARY') == None: continue  # skip blank items
            event.summary = component.get('SUMMARY')
            summary = event.summary
            event.uid = component.get('UID')
            uid = event.uid
            if component.get('DESCRIPTION') == None: continue  # skip blank items
            event.description = component.get('DESCRIPTION')
            description = event.description
            event.location = component.get('LOCATION')
            location = event.location
            if hasattr(component.get('dtstart'), 'dt'):
                event.start = component.get('dtstart').dt
                start_time= event.start
                print(type(start_time),start_time)
            if hasattr(component.get('dtend'), 'dt'):
                event.end = component.get('dtend').dt
                end_time = event.end
            event.url = component.get('URL')
            url = event.url
            #这里由于类关系的原因，不能直接处理today,duration,只能从mysql提取再处理一次
            #today = re_date(start_time)
            #print(today)

            table_structure = 'real_record(Summary,UID,Description,Location,from_v1,to_v1,URL)'
            value = "'{}','{}','{}','{}','{}','{}','{}'".format(summary,uid,description,location,start_time,end_time,url)
            mysql_tool.insert_info(table_structure, value)
            events.append(event)
            print(events)







read_ics()



