import matplotlib.pyplot as plt
from mysql_tool import Mysql_tool
import matplotlib.pyplot as plt  # 导入模块 matplotlib.pyplot，并简写成 plt
import numpy as np

mysql_tool = Mysql_tool()
s = mysql_tool.connect()

def make_circle():
    table_name = 'real_record'
    # 如果输入find_field，则为查找对应的字段
    find_field = 'summary,today,from_v1,time_long,portion_allday'
    # 如果办公设备查询条件，则是按条件查询
    # ?   该处取出的语句如何更智能化，？？？
    query_condition = "today like '20200528'"
    # 查询之后的数据进行一个处理程序
    result = mysql_tool.find_info(find_field, table_name, query_condition)
    n = 0
    for i in result:
        n += 1
        print(n,i)

    #饼状图
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

    labels = ['娱乐', '育儿', '饮食', '房贷', '交通', '其它']
    sizes = [2, 5, 12, 70, 2, 9]  # 比例
    explode = (0, 0, 0, 0.1, 0, 0)  # 让比例最高的离中心点远一点
    plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=False, startangle=150)
    plt.title("饼图示例-8月份家庭支出")
    plt.show()
    plt.axis('equal')  # 该行代码使饼图长宽相等


#绘制条形图
def zheXian_Chart():
    fig = plt.figure(figsize=(12, 6))
    # plt.subplot(121)
    # x = [0,1,2,3,4,5,6,7,8,9]
    # y = [0,2.3, 3.4, 1.2, 6.6, 7.0]
    # x = [range(0,10)]
    # y = [range(0,20)]
    x = [1, 2, 3, 4, 5]
    y = [2.3, 3.4, 1.2, 6.6, 7.0]
    # A 折线图
    plt.plot(x, y, color='r', linestyle='-')
    plt.subplot(1, 2, 1)
    plt.plot(x, y, color='r', linestyle='--')
    plt.show()

def bar_chart():


    table_name = 'real_record'
    # 如果输入find_field，则为查找对应的字段
    find_field = 'summary,today,from_v1,time_long,portion_allday'
    # 如果办公设备查询条件，则是按条件查询
    # ?   该处取出的语句如何更智能化，？？？
    query_condition = "today like '20200528'"
    # 查询之后的数据进行一个处理程序
    result = mysql_tool.find_info(find_field, table_name, query_condition)
    n = 0

    # val_ls = [np.random.randint(100) + i*20 for i in range(7)]
    scale_ls = range(20)
    #index_ls = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    index_ls = []
    # plt.bar(scale_ls, val_ls)

    y = []

    for search_result in result:
        n += 1
        list_result = list(search_result)
        #print(n, search_result)
        #print(type(list_result[0]))
        index_ls.append(list_result[0])
        y.append(list_result[3])



    # 创建一个点数为 8 x 6 的窗口, 并设置分辨率为 80像素/每英寸
    fig = plt.figure(figsize=(60, 80), dpi=300)


    # 外框设计，坐标

    fig, ax_lst = plt.subplots(1, 1)  # 创建一个以 axes 为单位的 2x2 网格的 figure

    # 设置横轴标签
    plt.xlabel("project")

    # 设置纵轴标签
    plt.ylabel("min")
    plt.xticks(scale_ls, index_ls)  ## 可以设置坐标字
    # plt.title('Average customer flows Number by Weekdays')

    plt.show()






if __name__ == '__main__':


    #make_circle()
    bar_chart()