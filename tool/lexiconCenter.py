import re
import os
import sys

# wechatBill 目录
BASE_DIR = os.path.dirname(os.path.abspath(__name__))
sys.path.append(BASE_DIR)

if sys.platform == 'linux':
    lexicon = '/tool/lexicon/'
elif sys.platform == 'win32':
    lexicon = '\\tool\\lexicon\\'

# 读取txt转成列表
def txtTOlist(file):

    data = []

    if not os.path.isfile(file):
        print('没有此文件!!')

    with open(file, mode='r', encoding='utf-8') as f:
        for i in f.readlines():
            data.append(i.strip('\n'))
    return set(data)


def lexiconList():

    '''

        wechatBill 词库中心

    餐饮酒店		cyjdNAME.txt
    餐饮			cycyNAME.txt
    ?????			kdgsNAME.txt
    品牌			ppNAME.txt
    全国省市区县	qgssqxNAME.txt
    ?????			spppNAME.txt
    垃圾食品        ljspNAME.txt
    交通工具        jtgjNAME.txt
    娱乐词库        yuleNAME.txt
    生活百科        shbkNAME.txt
    电子产品        dzcpNAME.txt
    :return:
    '''

    return ['cycyNAME.txt', 'qgssqxNAME.txt', 'ljspNAME.txt', 'cyjdNAME.txt', 'ppNAME.txt', 'jtgjNAME.txt', 'yuleNAME.txt', 'shbkNAME.txt', 'dzcpNAME.txt']

def currencyDiff(data, filelist):

    '''
    0. 获取词库数据 & 获取账单sql数据
    1. 词库撞库 账单数据
    2. 统计撞库关键字数量最高
    3. 统计撞库机率多少次
    '''

    matchList = []    # 匹配信息 列如:['巧克力', '泡芙']
    for msdata in txtTOlist(BASE_DIR+lexicon+'%s' % filelist):
        for wxdata in data:
            if not re.search(msdata, wxdata) == None:
                matchList.append(msdata)

    return matchList

class CITYNAME():
    '''
    城市词库接口
    '''

    def __init__(self, data):
        self.data = data

    def cityDiff(self):
        '''
        城市地名类接口
        :return:
        '''

        return currencyDiff(self.data, lexiconList()[1])

    def jtgjDiff(self):
        '''
        交通工具类接口
        :return:
        '''

        return currencyDiff(self.data, lexiconList()[5])

    def dzcpDiff(self):
        '''
        电子产品类接口
        :return:
        '''

    def shbkDiff(self):
        '''
        生活百科类接口
        :return:
        '''
        return currencyDiff(self.data, lexiconList()[7])

    def dzcpDiff(self):
        '''
        电子产品类接口
        :return:
        '''
        return currencyDiff(self.data, lexiconList()[8])


class CATENAME():
    '''
    美食词库接口
    '''

    def __init__(self, data):
        self.data = data

    def cateDiff(self):
        '''
        比对美食接口
        :return:
        '''
        return currencyDiff(self.data, lexiconList()[0])

    def ljspDiff(self):
        '''
        比对垃圾食品接口
        :return:
        '''
        return currencyDiff(self.data, lexiconList()[2])

    def yuleDiff(self):
        '''
        娱乐类接口
        :return:
        '''
        return currencyDiff(self.data, lexiconList()[6])

def COMPANYNAME():
    '''
    公司企业词库接口
    :return:
    '''

    def __init__(self, data):
        self.data = data

    def Diff():
        pass

if __name__ == '__main__':
    # txtTOlist('cymc.txt')

    # a = CATENAME(['麻辣烫'])
    print(BASE_DIR)