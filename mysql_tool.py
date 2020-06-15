import pymysql
import logging
from time import time
import pandas as pd
import time



class Mysql_tool():
    def __init__(self):
        self.host = "127.0.0.1"
        self.user = "root"
        self.passwd="abab11421992"
        self.db = "time_manage"
        self.port = 3306
        self.lg = logging.getLogger("Error")
    def connect(self):
        try:
            connect= pymysql.connect(host=self.host,
            user=self.user,
            passwd=self.passwd,
            db=self.db,
            port=self.port,
            charset='utf8mb4')
            return connect
        except Exception as e:
            self.lg.error(e)
    # 跳转连接到远方的服务器，该部分代码可根据后续的需要补齐
    def ssh_connect(self):
        pass
    #增加信息
    def insert_info(self,table_structure,values):
        connect= self.connect()
        cursor = connect.cursor()
        try:
            sql = "insert into {} values({})".format(table_structure, values)
            print(sql)
            cursor.execute(sql)
            connect.commit()
        except Exception as e:
            # rollbac in case there is any error
            connect.rollback()
            self.lg.error(e)
            cursor.close()
            connect.close()
    #更新信息
    def update_info(self,table_name, post_change,pro_change):
        connect = self.connect()
        cursor = connect.cursor()
        try:
            sql = "update {} set {} where {}".format(table_name, post_change,pro_change)
            print(sql)
            cursor.execute(sql)
            connect.commit()
        except Exception as e:
            #rollbac in case there is any error
            connect.rollback()
            self.lg.error(e)
            cursor.close()  #此处是否要缩进
            connect.close()
    # 查找信息
    def find_info(self,find_field, table_name,query_condition):
        connect = self.connect()
        cursor = connect.cursor()
        try:
        #1 查找全部的信息
            if len(find_field) == 0:
                sql = "select * from {}".format(table_name)
                print(sql)

            #2 根据某个字段来查找
            elif len(query_condition) == 0:
                sql = "select {} from {}".format(find_field,table_name)
                print(sql)
            #3 根据某个条件查找
            else:
                sql = "select {} from {} where {}".format(find_field, table_name,query_condition)
                print(sql)
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
            """for row in results:
            # 对查询出来的数据进行处理，该部分暂时不写，后续增加
            print(row)
            print(type(row))
            """
            connect.commit()
        except Exception as e:
            # rollbac in case there is any error
            connect.rollback()
            self.lg.error(e)
            cursor.close()
            connect.close()
    #删除信息
    def delete_info(self,table_name,query_condition,delete_condition):
        connect = self.connect()
        cursor = connect.cursor()
        try:
        #1 删除整张表
        #2 按条件删除信息
            if len(delete_condition) == 0:
                sql = "delete from {}".format(table_name)
                print(sql)
            else:
                sql = "delete from {} where {}".format(table_name,query_condition)
                print(sql)
                cursor.execute(sql)
                connect.commit()
        except Exception as e:
            connect.rollback()
            self.lg.error(e)
            cursor.close()
            connect.close()


"""if __name__ == '__main__':
    mysql_tool = Mysql_tool()
    #增加信息的sql语句需要传入的代码的例码
    table_structure = 'test(id,name,field)'
    #values = "12,'zuo','xin'"
    #此处添加多个参数可以写成这这种格式
    #中间不加单引号会形成1054错误
    #values = "'{}','{}','{}'".format(args1,args2,args3)
    #mysql_tool.insert_info(table_structure, values)
    #更新信息的样例和接口
    table_name = 'test'
    post_change = "name='xue'"
    pro_change = "name='xinxue'"
    #mysql_tool.update_info(table_name, post_change,pro_change)
    #查找信息 。该部分为查找的样例，后续需要增加功能 ，可以修改部分代码
    #访部分传参需要注意，table_name是必须要输入的，其他 两个则可以为为空，区别就是实现的功能不一样
    #该部分除如果传入表名，就是查找该表中的全部内容 ，
    table_name = 'test'
    #如果输入find_field，则为查找对应的字段
    find_field = 'id,name'
    #如果办公设备查询条件，则是按条件查询
    query_condition = "id > 1"
    #查询之后的数据进行一个处理程序
    #result = mysql_tool.find_info(find_field, table_name,query_condition)
    print(result)
    print(type(list(result)))
    for result in list(result):
    key = ''.join(list(result))
    #此处的类型为str
    print(type(key))
    #删除信息，目前考虑的是两种情况 ，后结如果有需要 可以增加
    #只传入tabel_name就会删除整个表格，
    table_name = 'test'
    #传入删除条件，就会按条件删除
    delete_condition = ""
    mysql_tool.delete_info(table_name,query_condition)
    """



if __name__ == '__main__':
    #passs
    """mysql_tool = Mysql_tool()
    table_name = 'sku'
    # 如果输入find_field，则为查找对应的字段
    find_field = 'sku'
    # 如果办公设备查询条件，则是按条件查询
    query_condition = ""
    mysql_tool.find_info(find_field, table_name,query_condition)
    """

    """
    mysql_tool = Mysql_tool()
    #s=mysql_tool.connect()
    #print(s)
    table_name = 'time_record'
    # 如果输入find_field，则为查找对应的字段
    find_field = 'classification_v1,duration'
    # 如果办公设备查询条件，则是按条件查询
    query_condition = " today like '2020_05_09' "
    # 查询之后的数据进行一个处理程序
    result = mysql_tool.find_info(find_field, table_name, query_condition)
    # print(result)
    """
