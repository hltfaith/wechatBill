# -*- coding:utf-8 -*-
import csv
import sqlite3
import os

def checkFile():
    pass

def getfile():

    '''
    获取用户上传后的账单文件
    :return:  判断长度为0,表示用户提交文件格式有误或提交为空
    '''

    uploadlist = []
    filelist = []

    for file in os.listdir('static/uploads/'):
        uploadlist.append(file)

    for i in uploadlist:
        filename, filetype = os.path.splitext(i)
        if filetype == '.csv':
            filelist.append(i)

    return filelist

def createDB():

    '''
    初始化数据库，创建数据表
    :return:
    '''

    if not os.path.isfile('wxbill.db'):
        conn = sqlite3.connect('wxbill.db')
        sql = conn.cursor()
        sql.execute('''
        CREATE TABLE BILL(
   ID INT PRIMARY KEY     NOT NULL,
   JYSJ           DATETIME,
   JYLX           TEXT,
   JYDF           TEXT,
   SP             TEXT,
   SZ             TEXT,
   JE             INT,
   ZFFS           TEXT,
   DQZT           TEXT,
   JYDH           TEXT,
   SPDH           TEXT,
   BZ             TEXT
);''')

        importData(sql)
    else:
        conn = sqlite3.connect('wxbill.db')
        sql = conn.cursor()
        importData(sql)

    conn.commit()
    print('DATA import SUCCESS!')
    conn.close()

def importData(sql):

    '''

    账单分析
    导入支付账单到sqlite3数据库中

    :param sql:
    :return:
    '''

    if not len(getfile()) == 0:

        id = 1

        for data in getfile():

            csv_file = csv.reader(open('static/uploads/'+data, 'r', encoding='utf-8'))

            count = 1
            for line in csv_file:
                if count >= 18:
                    sql.execute("INSERT INTO BILL (ID,JYSJ,JYLX,JYDF,SP,SZ,JE,ZFFS,DQZT,JYDH,SPDH,BZ) \
              VALUES ('%d', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (id, line[0], line[1], line[2], line[3],
                    line[4], str(line[5][1:]).replace(',', ''), line[6],  line[7],  line[8],  line[9],  line[10]))

                    id += 1
                count += 1


def get_wx_name():

    '''
    微信账单 获取微信昵称
    :return:
    '''

    data = getfile()

    csv_file = csv.reader(open('static/uploads/' + data[0], 'r', encoding='utf-8'))

    count = 1
    wx_name = []
    for line in csv_file:
        if count == 2:
            wx_name.append(line[0][6::][:-1])

        count += 1

    return wx_name

def test():

    '''
        测试类  用于程序调试
    :return:
    '''

    print(getfile())


if __name__ == '__main__':

    # 创建数据库
    createDB()

    # 测试程序
    # test()
