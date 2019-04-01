# -*- coding:utf-8 -*-
import datetime
import os
import hashlib
import re
import time
import sys
import io
import random
import shutil

'''
其实print()函数的局限就是Python默认编码的局限，因为系统是win7的，python的默认编码不是'utf-8',改一下python的默认编码成'utf-8'就行了
'''

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')   # 改变标准输出的默认编码

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from tool.lexiconCenter import CATENAME, CITYNAME

# 工具类

def get_time_list(start, end):

    '''

    比对时间段中日期

    :param start:
    :param end:
    :param current:
    :return: 返回列表, 没有消费的日期
    '''

    date_list = []
    date = datetime.datetime.strptime(start, '%Y-%m-%d')
    end = datetime.datetime.strptime(end, '%Y-%m-%d')
    while date <= end:
        date_list.append(date.strftime('%Y-%m-%d'))
        date = date + datetime.timedelta(1)

    return date_list

def get_date_list(start, end, current):

    '''

    比对时间段中日期

    :param start:
    :param end:
    :param current:
    :return: 返回列表, 没有消费的日期
    '''

    date_list = []
    date = datetime.datetime.strptime(start, '%Y-%m-%d')
    end = datetime.datetime.strptime(end, '%Y-%m-%d')
    while date <= end:
        date_list.append(date.strftime('%Y-%m-%d'))
        date = date + datetime.timedelta(1)

    lack_date = []
    for i in date_list:
        if not i in current:
            lack_date.append(i)

    return lack_date

def like_thing_list(likeList):

    '''

    比对最爱吃的东西

    :param likeList:
    :return:
    '''

    newNum = []

    num_list = []
    for i in likeList:
        num_list.append(likeList.count(i))

    for i in likeList:
        if likeList.count(i) == max(num_list):
            newNum.append(i)

    return list(set(newNum))

def weekly_thing_list(zgxf, zdxf, sumxf):

    '''

    通过周一 + 7天 方式得出一周消费金额

    1. 判断日期为第几周
    2. 通过第几周 生成一周消费金额
    3. 最低、最高两周对比

    :param zgxf:
    :param zdxf:
    :param sumxf:
    :return:

    '''

    zgxf_num = []
    zdxf_num = []

    for i in sumxf:
        if i[1] == zgxf[0]:
            zgxf_num.append(i[2])

    for i in sumxf:
        if i[1] == zdxf[0]:
            zdxf_num.append(i[2])

    if not len(zdxf_num) > 7:
        count = 7 - len(zdxf_num)
        for i in range(0, count):
            zdxf_num.append(0)

    count_num = [zgxf_num, zdxf_num]

    return count_num

def get_consume_classify(month, data):

    '''

    半年消费分类

    需求：
        0. 每一消费类型, 求出消费金额
        1. 获取近七个月的数据

    步骤如下：
        0. 获取所有月份
        1. 获取 金额 交易对方 月份
        2. 美食 交通 娱乐 生活 电子产品  5个方面撞库
        2. 获取当前月 [美食$ 交通$ 娱乐$ 生活$ 电子产品$] 金额

    原则标准：
        -- 判断最小月 < 3月  输出 [1, 2, 3, 4, 5, 6, 7]
        -- 判断最中月 >=3月  输出 [3, 4, 5, 6, 7, 8, 9]
        -- 判断最大月 >=8月  输出 [6, 7, 8, 9 ,10, 11, 12]
    :return:

    '''

    # 获取月份
    monthMax = []
    for i in month:
        monthMax.append(int(i))

    # 月份列表
    monthList = []          # monthList[0]       stdout [1, 2, 3, 4, 5, 6, 7]
    if min(monthMax) >= 8:
        monthList.append([6, 7, 8, 9, 10, 11, 12])
    elif min(monthMax) >= 3:
        monthList.append([3, 4, 5, 6, 7, 8, 9])
    elif min(monthMax) < 3:
        monthList.append([1, 2, 3, 4, 5, 6, 7])

    # 获取数据 [金额 交易对方 月份]
    get_data = []
    for i in data:
        get_data.append(i[1])

    # 美食 交通 娱乐 生活 电子产品 撞库
    meishi = CATENAME(get_data).cateDiff()
    jiaotong = CITYNAME(get_data).jtgjDiff()
    yule = CATENAME(get_data).yuleDiff()
    shenghuo = CITYNAME(get_data).shbkDiff()
    dzcp = CITYNAME(get_data).dzcpDiff()

    # 获取当前月 [美食$ 交通$ 娱乐$ 生活$ 电子产品$] 金额
    # 月中的数据
    get_month = []

    classifyList = ['美食', '交通', '娱乐', '生活', '电子产品']

    for classify in classifyList:  # [0, 1, 2, 3, 4]  美食 交通 娱乐 生活 电子产品

        if classify == '美食':
            ms = []
            for month in monthList[0]:  # [1, 2, 3, 4, 5, 6, 7] 半年美食的消费金额

                if month in monthMax:  # [2, 3]

                    pp_ms = []
                    for cate in set(meishi):  # [餐饮 翠清 豪杰 麦当劳]
                            for k in data:      # [6, '全时便利店', '02']
                                if re.search(cate, k[1]):   # 判断匹配到的美食 在当前月列表中
                                    if month == int(k[2]):   # 匹配月份
                                        pp_ms.append(k[0])
                    ms.append(sum(pp_ms))
                else:
                    # 不再账单中的月份
                    ms.append(0)

            get_month.append(ms)

        elif classify == '交通':
            jt = []
            for month in monthList[0]:  # [1, 2, 3, 4, 5, 6, 7] 半年美食的消费金额

                if month in monthMax:   # [2, 3]
                    pp_ms = []
                    for cate in set(jiaotong):  # [餐饮 翠清 豪杰 麦当劳]
                            for k in data:      # [6, '全时便利店', '02']
                                if re.search(cate, k[1]):   # 判断匹配到的美食 在当前月列表中
                                    if month == int(k[2]):   # 匹配月份
                                        pp_ms.append(k[0])
                    jt.append(sum(pp_ms))

                else:
                    # 不再账单中的月份
                    jt.append(0)

            get_month.append(jt)

        elif classify == '娱乐':
            yl = []
            for month in monthList[0]:  # [1, 2, 3, 4, 5, 6, 7] 半年美食的消费金额

                if month in monthMax:   # [2, 3]
                    pp_ms = []
                    for cate in set(yule):  # [餐饮 翠清 豪杰 麦当劳]
                            for k in data:      # [6, '全时便利店', '02']
                                if re.search(cate, k[1]):   # 判断匹配到的美食 在当前月列表中
                                    if month == int(k[2]):   # 匹配月份
                                        pp_ms.append(k[0])
                    yl.append(sum(pp_ms))

                else:
                    # 不再账单中的月份
                    yl.append(0)

            get_month.append(yl)

        elif classify == '生活':
            sh = []
            for month in monthList[0]:  # [1, 2, 3, 4, 5, 6, 7] 半年美食的消费金额

                if month in monthMax:   # [2, 3]
                    pp_ms = []
                    for cate in set(shenghuo):  # [餐饮 翠清 豪杰 麦当劳]
                            for k in data:      # [6, '全时便利店', '02']
                                if re.search(cate, k[1]):   # 判断匹配到的美食 在当前月列表中
                                    if month == int(k[2]):   # 匹配月份
                                        pp_ms.append(k[0])
                    sh.append(sum(pp_ms))

                else:
                    # 不再账单中的月份
                    sh.append(0)

            get_month.append(sh)

        elif classify == '电子产品':
            dz = []
            for month in monthList[0]:  # [1, 2, 3, 4, 5, 6, 7] 半年美食的消费金额

                if month in monthMax:   # [2, 3]
                    pp_ms = []
                    for cate in set(dzcp):  # [餐饮 翠清 豪杰 麦当劳]
                            for k in data:      # [6, '全时便利店', '02']
                                if re.search(cate, k[1]):   # 判断匹配到的美食 在当前月列表中
                                    if month == int(k[2]):   # 匹配月份
                                        pp_ms.append(k[0])
                    dz.append(sum(pp_ms))

                else:
                    # 不再账单中的月份
                    dz.append(0)

            get_month.append(dz)

    # print(get_month)
    # print(monthList[0])

    return monthList[0], get_month

def get_xfzgyzsz(zgxfzc, zgxfsr):

    '''

    消费最高一周收支记录

    需求：
        1. 周一至周日 支出 收入  盈利
        2. 展现形式
                1).  支出data:[-120, -132, -101, -134, -190, -230, -210]  周一至周日

    :param sumxf:
    :param zgxfzc:
    :param zgxfsr:
    :return:

    '''

    # 存储一周支出金额 [-120, -132, -101, -134, -190, -230, -210]
    zgxfzc_list = []

    # 存储一周收入金额 [320, 302, 341, 374, 390, 450, 420]
    zgxfsr_list = []

    weekList = [1, 2, 3, 4, 5, 6, 0]

    # 解包: 收入  [1,2,3,4] 周几
    weeksr_list = []
    for weeksr in zgxfsr:
        weeksr_list.append(int(weeksr[0]))

    # 累计收入
    for week in weekList:

        if week in weeksr_list:

            for sr in zgxfsr:
                if week == int(sr[0]):
                    zgxfsr_list.append(sr[1])

        else:
            zgxfsr_list.append(0)

    # 解包: 支出  [1,2,3,4] 周几
    weekzc_list = []
    for weekzc in zgxfzc:
        weekzc_list.append(int(weekzc[0]))

    # 累计各周支出
    for week in weekList:
        if week in weekzc_list:
            for zc in zgxfzc:
                if week == int(zc[0]):
                    zgxfzc_list.append(-zc[1])
        else:
            zgxfzc_list.append(0)

    return zgxfzc_list, zgxfsr_list

def get_year_month_sz(year_month_pay, year_month_income):

    '''

    全年各月收支记录

    需求：
        1. 各月支出、收入 金额
        2. 最大金额 + 100

    实现
        支出 data:[2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]

    :param year_month_pay:
    :param year_month_income:
    :return:  maxvalue, monthpay_list, monthincome_list

    '''

    # stdout    [['02', 6635.63], ['03', 3006.65]]

    # 全年月份
    monthzs_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    # 各月支出
    monthpay_list = []

    # 各月收入
    monthincome_list = []

    # 解包: 支出  [1,2,3,4] 月份
    monthz_list = []
    for pay in year_month_pay:
        monthz_list.append(int(pay[0]))

    # 累计各月支出
    for month in monthzs_list:
        if month in monthz_list:

            for sr in year_month_pay:
                if month == int(sr[0]):
                    monthpay_list.append(sr[1])

        else:
            monthpay_list.append(0)

    # 解包: 收入  [1,2,3,4] 月份
    months_list = []
    for income in year_month_income:
        months_list.append(int(income[0]))

    # 累计各月支出
    for month in monthzs_list:
        if month in months_list:
            for sr in year_month_income:
                if month == int(sr[0]):
                    monthincome_list.append(sr[1])
        else:
            monthincome_list.append(0)

    # 最大值
    maxvalue = []
    if max(monthpay_list) > max(monthincome_list):
        maxvalue.append(max(monthpay_list)+100)
    else:
        maxvalue.append(max(monthincome_list)+100)

    return maxvalue, monthpay_list, monthincome_list

def get_xffb_jcxfsp(cate, data):

    '''

    经常消费商铺

    需求：
        1. 商铺名称
        2. 次数数量
        3. 前五个

    :return:
    '''

    jcxfsp_list = []

    # 获取商铺列表
    sp_list = []
    for i in set(cate):
        for db in data:
            if re.search(i, db):
                sp_list.append(db)

    # 商铺与数量
    sp_count = []
    for i in set(sp_list):
        sp_count.append([sp_list.count(i), i])

    count = 1
    sp_count.sort(reverse=True)
    for i in sp_count:
        if count <= 5:
            jcxfsp_list.append([i[0], i[1]])
        count += 1

    return jcxfsp_list

def get_xffb_xfqy(city):

    '''

    当前区域商铺

    :param city:
    :return:
    '''

    sp_count = []
    for i in set(city):
        sp_count.append([city.count(i), i])

    sp_count.sort(reverse=True)

    if not len(sp_count) >= 5:
        count = 5 - len(sp_count)
        for i in range(0, count):
            sp_count.append([0, ''])

    return sp_count

def get_random_values():

    '''
        微信账单 称号 随机值
    :return:
    '''

    titleList = [

        '消费不理智',
        '消费很过分',
        '消费很狂躁',
        '消费一股清流',
        '消费小书生',
        '只能用钱形容',
        '不忍直视呀',
        '兜里还有钱吗',
        '坐等吃土',
        '真TMD有钱',
        '和马云是朋友'
    ]

    return random.choice(titleList)

def get_hydj_values(zjls):

    '''
            微信账单 会员等级
            会员等级：
                    黑卡用户        10万+
                    至尊用户        7万+
                    白领用户        4万+
                    小资用户        2万+
                    VIP用户         1万+
                    普通用户        5千+
                    穷鬼用户        1K
    :return:
    '''

    hydj = []

    if zjls[0] >= 100000:
        hydj.append('黑卡用户')
    elif zjls[0] >= 70000:
        hydj.append('至尊用户')
    elif zjls[0] >= 40000:
        hydj.append('白领用户')
    elif zjls[0] >= 20000:
        hydj.append('小资用户')
    elif zjls[0] >= 10000:
        hydj.append('VIP用户')
    elif zjls[0] >= 5000:
        hydj.append('普通用户')
    elif zjls[0] >= 1000:
        hydj.append('穷鬼用户')

    return hydj

def get_current_time():

    '''

    微信账单 获取当前时间

    :return:
    '''

    return time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))

def get_access_count():

    '''

    微信账单获取 访问第几位用户   流水帐号

    :return:
    '''

    with open(BASE_DIR+'/tool/token', 'r') as f:
        value = f.readlines()

    fwls = [int(value[0]), 1000000000000000000 + int(value[0])]

    return fwls

def set_access_count():

    '''

    微信账单 设置访问第几位用户

    :return:
    '''

    newAccess = int(get_access_count()[0]) + 1

    with open(BASE_DIR+'/tool/token', 'w') as f:
        f.write(str(newAccess))

    f.close()

def active_local_map():
    pass

def get_file_md5(filename, *args):

    '''
    判断文件
    MD5                               File
    4a90e095136711e0a6e8a8b2f6118d35  columnarChart.js
    9568555b02f5704a83dd778ec0172b62  indexChart.js
    ab5c6dda5cf470d21d5405a691f8e3ce  pieChart.js
    68e1a59ca4c62983f7e4ff601fe7cbdd  wechatBill.md

    *args

    :return:
    '''

    if sys.platform == 'linux' and str(*args) == 'new':
        file = '/static/js/charts/' + filename

    elif sys.platform == 'linux' and str(*args) == 'old':
        file = '/static/chartbak/' + filename

    elif sys.platform == 'win32' and str(*args) == 'new':
        file = '//static//js//charts//' + filename

    elif sys.platform == 'win32' and str(*args) == 'old':
        file = '//static//chartbak//' + filename

    if not os.path.isfile(BASE_DIR+file):
        print('没有此文件!')

    myhash = hashlib.md5()
    f = open(BASE_DIR+file, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()

    return myhash.hexdigest()


def copy2File(srcfile, dstfile):
    '''
    拷贝文件
    :param srcfile:
    :param dstfile:
    :return:
    '''

    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径
        shutil.copyfile(srcfile, dstfile)  # 复制文件
        # print("copy %s -> %s" % (srcfile, dstfile))


def export_bill_docx():

    '''

    微信账单 docx文件格式导出

    :return:
    '''

    userBill_DIR = BASE_DIR+'/static/js/charts/wechatBill.md'
    exportBill_DIR = BASE_DIR+'/static/doc/wechatBill.md'
    exportDocx_DIR = BASE_DIR+'/static/doc/wechatBill.docx'

    copy2File(userBill_DIR, exportBill_DIR)

    newfile = []
    with open(BASE_DIR + '/static/doc/wechatBill.md', 'r', encoding='utf-8') as f:
        a = f.readlines()

        for line in a:
            if re.search("&#160;", line):
                a = line.replace("&#160;", "")
                newfile.append(a)

            elif re.search("---------------------------------------------------------------------------------------------------------", line):
                a = line.replace("---------------------------------------------------------------------------------------------------------"
                                 , "-------------------------------------------------------------------------------------")
                newfile.append(a)

            elif re.search("~~", line):
                a = line.replace("~~", "")
                newfile.append(a)

            else:
                newfile.append(line)

    f.close()


    with open(exportBill_DIR, 'w', encoding='utf-8') as new:

        for i in newfile:
            new.write(i)

    new.close()

    os.system('pandoc %s -o %s' % (exportBill_DIR, exportDocx_DIR))


def test():

    '''

        测试方法, 用于程序调试

    :return:
    '''

    # print(get_random_values())

    # zjls = [35174.27]
    # print(get_hydj_values(zjls))

    # print(set_access_count())
    # set_access_count()

    export_bill_docx()

if __name__ == '__main__':

    # 测试类方法
    test()
