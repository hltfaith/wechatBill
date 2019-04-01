import sqlite3
from tool import analyseTools
from tool.lexiconCenter import CATENAME
from tool.lexiconCenter import CITYNAME
from getData import get_wx_name

'''
其实print()函数的局限就是Python默认编码的局限，因为系统是win7的，python的默认编码不是'utf-8',改一下python的默认编码成'utf-8'就行了
'''
# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')   # 改变标准输出的默认编码


def connDB():

    '''
    连接sqlite3数据库
    :return:
    '''

    conn = sqlite3.connect('wxbill.db')
    sql = conn.cursor()

    return sql

def connSQL(*args):
    return args

def connOFF():
    pass

class DBAPI():

    def __init__(self):
        self.sql = connDB()

    # 消费记录
    def queryCONSUME(self, *args):
        '''
            ##查询需求##                    ##查询代码##
        0. 最高消费金额日期                 (moneyTime)
        1. 消费最高一次金额                 (money)
        2. 最晚的一次消费                   (zwxf)
        3. 平均每天至少消费几次             (zsxf_num)
        4. 其中有几天没有消费               (daywxf)
        5. 中午时间段消费多少笔11:00~13:30  (noon_xf_num)
        6. 早上时间段消费多少笔06:00~09:30  (morn_xf_num)
        7. 晚上时间消费多少笔18:00~24:00    (night_xf_num)
        8. 平均每天消费多少金额             (avg_day_xf)
        9. 收发红包次数                     (sf_redpacket_num)

        :param args: 输入相应功能编码
        :return: 返回查询内容段
        '''

        data = ()
        try:
            if str(args[0]) == 'money':
                # 最高消费金额
                data = self.sql.execute("SELECT max(JE) FROM bill;")
            elif str(args[0]) == 'moneyTime':
                # 最高消费日期
                data = self.sql.execute("SELECT JYSJ FROM BILL WHERE JE == (SELECT max(JE) FROM bill);")

            elif str(args[0]) == 'zsxf_num':
                # 平均每天至少消费几次
                data = self.sql.execute(
                    "SELECT ((SELECT count(JYSJ) FROM bill) / (SELECT count(DISTINCT strftime('%Y-%m-%d',JYSJ)) FROM bill));")

            elif str(args[0]) == 'zwxf':
                # 最晚的一次消费
                data1 = self.sql.execute("SELECT max(JYSJ) FROM bill WHERE strftime('%H:%M:%S',JYSJ) < '06:00:00';")

                data1_num = []
                for i in data1:
                    data1_num = i

                if data1_num[0] is None:
                    data = self.sql.execute(
                        "SELECT strftime('%Y-%m-%d ', JYSJ) || max(strftime('%H:%M:%S',JYSJ)) FROM bill WHERE strftime('%H:%M:%S',JYSJ) < '24:00:00';")
                else:
                    data = self.sql.execute("SELECT max(JYSJ) FROM bill WHERE strftime('%H:%M:%S',JYSJ) < '06:00:00';")

            elif str(args[0]) == 'daywxf':
                # 其中几天没有消费
                start_day = ''
                end_day = ''
                current = []

                for start in self.sql.execute("SELECT min(DISTINCT strftime('%Y-%m-%d',JYSJ)) FROM bill;"):
                    start_day = start[0]

                for end in self.sql.execute("SELECT max(DISTINCT strftime('%Y-%m-%d',JYSJ)) FROM bill;"):
                    end_day = end[0]

                for curr in self.sql.execute("SELECT DISTINCT strftime('%Y-%m-%d',JYSJ) FROM bill;"):
                    current.append(curr[0])

                # 接口文件
                sum_l1 = []
                l1 = []
                for i in analyseTools.get_date_list(start_day, end_day, current):
                    l1.append([i, 0])

                for i in l1:
                    sum_l1.append(i)

                # data = sum_l1

                return [start_day, end_day, len(sum_l1)]

            elif str(args[0]) == 'morn_xf_num':
                # 早上时间段消费多少笔06:00~09:30
                data = self.sql.execute(
                    "SELECT count(JYSJ) FROM bill WHERE strftime('%H:%M:%S',JYSJ) BETWEEN '06:00:00' AND '09:30:00';")

            elif str(args[0]) == 'noon_xf_num':
                # 中午时间段消费多少笔11:00~13:30
                data = self.sql.execute(
                    "SELECT count(JYSJ) FROM bill WHERE strftime('%H:%M:%S',JYSJ) BETWEEN '11:00:00' AND '13:30:00';")

            elif str(args[0]) == 'night_xf_num':
                # 晚上时间段消费多少笔18:00~24:00
                data = self.sql.execute(
                    "SELECT count(JYSJ) FROM bill WHERE strftime('%H:%M:%S',JYSJ) BETWEEN '18:00:00' AND '23:59:59';")

            elif str(args[0]) == 'avg_day_xf':
                # 平均每天消费多少金额
                data = self.sql.execute(
                    "SELECT ((SELECT SUM(JE) FROM bill WHERE SZ='支出') / (SELECT count(DISTINCT strftime('%Y-%m-%d',JYSJ)) FROM bill));")

            elif str(args[0]) == 'sf_redpacket_num':
                # 收发红包次数  转账

                num = []  # [6, 1] 收, 发, 收到最大金额, 发送最大金额 , 转账次数, 转最大金额, 收最大金额
                for i in self.sql.execute("SELECT count(*) FROM bill WHERE JYLX = '微信红包' AND SZ = '收入';"):
                    num.append(i)

                for i in self.sql.execute("SELECT count(*) FROM bill WHERE JYLX = '微信红包' AND SZ = '支出';"):
                    num.append(i)

                for i in self.sql.execute("select max(JE) from bill where JYLX = '微信红包' and SZ = '收入';"):
                    num.append(i)

                for i in self.sql.execute("select max(JE) from bill where JYLX = '微信红包' and SZ = '支出';"):
                    num.append(i)

                for i in self.sql.execute("select count(*) from bill where JYLX = '转账';"):
                    num.append(i)

                for i in self.sql.execute("select max(JE) from bill where JYLX = '转账' and SZ = '支出';"):
                    num.append(i)

                for i in self.sql.execute("select max(JE) from bill where JYLX = '转账' and SZ = '收入';"):
                    num.append(i)

                data = num

            else:
                print('Input Error!')
        except IndexError:
            pass

        value = []
        for i in data:
            value.append(i[0])

        return value

    # 预测查询
    def queryForecast(self, *args):

        '''
        预测功能
          ##查询需求##                 ##查询代码##
        1. 预测生活规律               (law_of_life)
        2. 预测所在领域               (local)
        3. 特别的一天                 (special_day)
        4. 预测最爱吃的东西           (like_thing)
        5. 预测每周、每月固定做的事情 (weekly_thing / monthly_thing)
        :return:
        '''

        value = []

        try:

            if str(args[0]) == 'like_thing':
                # 最爱吃的东西
                data = self.sql.execute("select SP from bill;")
                num = []
                for i in data:
                    num.append(i[0])

                # 匹配到喜欢吃的东西
                matchData = CATENAME(num).cateDiff()
                # 精确数量最多的事物
                value = analyseTools.like_thing_list(matchData)

            elif str(args[0]) == 'local':
                # 预测所在城市
                data = self.sql.execute("select JYDF from bill where  JYDF NOT like '%外卖%' and NOT JYDF == '上海拉扎斯信息科技有限公司';")
                num = []
                for i in data:
                    num.append(i[0])

                # 匹配到城市
                matchData = CITYNAME(num).cityDiff()
                # 精确数量最多的城市
                value = analyseTools.like_thing_list(matchData)

            elif str(args[0]) == 'weekly_thing':
                # 预测每周固定做的事情
                data = self.sql.execute("select strftime('%Y-%m-%d',JYSJ),strftime('%w',JYSJ), JYDF, SP from bill where NOT JYDF == '/' and NOT SP == '/';")
                num = []
                for i in data:
                    num.append(i)

                #print(num)
                # 一段日期拆出周一 ~ 周日



            elif str(args[0]) == 'monthly_thing':
                # 预测每月固定做的事情
                pass

            elif str(args[0]) == 'special_day':
                # 预测特别的一天

                # 生日
                data_sr = self.sql.execute(
                    "select JYSJ, JYDF, SP from bill where JYDF LIKE '%生日%' or JYDF LIKE '%蛋糕%' or SP LIKE '%生日%' or SP LIKE '%蛋糕%' LIMIT 1;")

                data_sr_list = []
                data_hb_list = []
                data_countnum_list = []
                data_countxf_list = []

                for i in data_sr:
                    data_sr_list.append(i)

                if len(data_sr_list):
                    value = data_sr_list

                else:
                    data_hb = self.sql.execute(
                        "select strftime('%Y-%m-%d',JYSJ), Count(strftime('%Y-%m-%d',JYSJ)) from bill where JYLX == '微信红包' group by strftime('%Y-%m-%d',JYSJ) ORDER BY COUNT(strftime('%Y-%m-%d',JYSJ)) DESC LIMIT 1;")

                    for i in data_hb:
                        data_hb_list.append(i)

                    if len(data_hb_list):
                        value = data_hb_list

                    else:
                        data_countnum = self.sql.execute(
                            "select strftime('%Y-%m-%d',JYSJ),Count(strftime('%Y-%m-%d',JYSJ)) from bill group by strftime('%Y-%m-%d',JYSJ) ORDER BY COUNT(strftime('%Y-%m-%d',JYSJ)) DESC LIMIT 1;")

                        for i in data_countnum:
                            data_countnum_list.append(i)

                        if len(data_countnum_list):
                            value = data_countnum_list

                        else:
                            data_countxf = self.sql.execute(
                                "select strftime('%Y-%m-%d',JYSJ),SUM(JE) from bill GROUP BY strftime('%Y-%m-%d',JYSJ) ORDER BY SUM(JE) DESC LIMIT 1;")

                            for i in data_countxf:
                                data_countxf_list.append(i)

                            if len(data_countxf_list):
                                value = data_countxf_list

            else:
                print('Input Error!')

        except IndexError:
            pass

        return value

    # 生活事件查询
    def queryLife(self, *args):
        '''
        1. 酒店次数               (jd_num)
        2. 飞机出行次数, 火车出行 (fj_num)
        5. 滴滴打车次数           (didi_num)
        6. 乘坐地铁次数           (subway_num)
        7. 外卖订单次数           (waimai_num)
        8. 年轻人不要吃太多垃圾食品注意饮食，共吃了肯德基 麦当劳次数, 占当前吃饭总数的百分之几 (ljsp_num)
        9. 医院次数               (yiyuan_num)

        :return:
        '''

        value = []

        try:

            if str(args[0]) == 'didi_num':
                # 滴滴打车次数

                data = self.sql.execute("select count(JYDF) from bill where JYDF LIKE '%滴滴%';")
                num = []
                for i in data:
                    num.append(i[0])
                value = num

            elif str(args[0]) == 'subway_num':
                # 乘坐地铁次数

                data = self.sql.execute("select count(SP) from bill where SP LIKE '%地铁%' or JYDF LIKE '%北京轨道交通%';")
                num = []
                for i in data:
                    num.append(i[0])
                value = num

            elif str(args[0]) == 'waimai_num':
                # 外卖订单次数

                data = self.sql.execute("select count(SP) from bill where SP LIKE '%外卖%' or JYDF LIKE '%上海拉扎斯信息科技有限公司%';")
                num = []
                for i in data:
                    num.append(i[0])
                value = num

            elif str(args[0]) == 'yiyuan_num':
                # 医院次数

                data = self.sql.execute(
                    "select count(SP) from bill where SP LIKE '%医院%' or JYDF LIKE '%医院%' or JYDF LIKE '%门诊%';")
                num = []
                for i in data:
                    num.append(i[0])
                value = num

            elif str(args[0]) == 'ljsp_num':
                # 垃圾食品次数
                data = self.sql.execute("select SP from bill where NOT SP == '/' and NOT SP == '收款方备注:二维码收款' and NOT SP == '转账备注:微信转账' and NOT SP == '条码支付';")

                num = []
                for i in data:
                    num.append(i[0])
                result = CATENAME(num).ljspDiff()

                # 吃垃圾食品的次数
                count = 0
                for i in result:
                    count += 1

                # 占月吃饭的百分之几

                bfj = count / 93

                value.append([count, bfj])

            elif str(args[0]) == 'fj_num':
                # 飞机出行次数

                data = self.sql.execute(
                    "select COUNT(SP) from BILL where SP LIKE '%机票%' or SP LIKE '%飞机%' or SP LIKE '%航空%';")
                num = []
                for i in data:
                    num.append(i[0])
                value = num

            elif str(args[0]) == 'jd_num':
                # 酒店次数

                data = self.sql.execute(
                    "select COUNT(SP) from bill where SP LIKE '%酒店%' or JYDF LIKE '%酒店%' or SP LIKE '%宾馆%' or JYDF LIKE '%宾馆%';")
                num = []
                for i in data:
                    num.append(i[0])
                value = num

            else:
                print('Input Error!')

        except IndexError:
            pass


        return value

    def queryFootmark(self, *args):

        '''
        6. 城市足迹, 10个活跃的地点       (footmark_10top)
        2. 消费记录图展现活跃地点          (active_local)
        11. 假期为所在地的GDP贡献总值      (gdp_sum)
        :param args:
        :return:
        '''

        value = []

        try:
            if str(args[0]) == 'footmark_10top':
                data = self.sql.execute("select JYDF from bill where NOT JYDF == '/' and  JYDF NOT like '%上海拉扎斯信息科技有限公司%' and  JYDF NOT like '%银行%' and  JYDF NOT like '%北京轨道交通%' and  JYDF NOT like '%携程%' and  JYDF NOT like '%手机充值%' and  JYDF NOT like '%滴滴%' group by JYDF ORDER BY count(JYDF) DESC;")

                num = []
                for i in data:
                    num.append(i[0])

                citydiff = CITYNAME(num).cityDiff()
                value = set(citydiff)


            elif str(args[0]) == 'active_local':
                pass

            elif str(args[0]) == 'gdp_sum':
                pass

            else:
                print('Input Error!')

        except IndexError:
            pass

        return value

    def queryForeEnd(self, *args):

        '''
        页面前端展现数据

        1. 支出明细             (zcmx)
            1). 共 多少 条记录  (zcmx_jl)

        2. 支出预览             (zcyl_zs)
            1).总支出           (zcyl_zzc)
            2).总收入           (zcyl_zsr)
            3).单笔最高支出       (zcyl_dbzgzc)
            4).单笔最高收入       (zcyl_dbzgsr)
            5).单笔最高支出百分比  (zcyl_dbzgzcbfb)
            6).单笔最高收入百分比  (zcyl_dbzgsrbfb)

            消费分类
            1). 美食              (zcyl_ms)
            2). 交通              (zcyl_jt)
            3). 娱乐              (zcyl_yl)
            4). 生活              (zcyl_sh)
            5). 电子产品           (zcyl_dzcp)

            近一周消费
            1). 日期              (zcyl_rq)
            2). 金额              (zcyl_je)

            两周高低消费对比
            1). 总消费             (zcyl_zxf)
                2). 最低日期
                3). 最高日期

            TOP10 消费清单         (zcyl_xftop10)

        3. 消费支收
            1). 半年消费分类        (xfzs_bnxffl)
            2). 消费最高一周收支记录  (xfzs_xfzgyzsz)
            3). 全年各月收支记录     (xfzs_qngysz)

        4. 消费分布
            1). 消费区域            (xffb_xfqy)
            2). 经常消费商铺        (xffb_jcxfsp)
            3). 日常生活            (xffb_rcsh)
            4). 钱都去了哪里         (xffb_qdqlnl)

        :param args:
        :return:
        '''

        value = []

        try:

            if str(args[0]) == 'zcmx':
                # 支出明细页面

                data = self.sql.execute("select ID,SP,JYLX,JE,JYSJ,JYDH from bill;")

                num = [['ID', 'SP', 'JYLX', 'JE', 'JYSJ', 'JYDH']]
                # count = 0
                for i in data:
                    i5 = str(i[5]).replace('\t', '')
                    num.append([i[0], i[1], i[2], i[3], i[4], i5])
                    # num.append([count, i[1], i[2], i[3], i[4], i5])
                    # count += 1

                value = num

            elif str(args[0]) == 'zcmx_jl':
                # 支出明细 共多少条记录
                num = []
                for i in self.sql.execute("select COUNT(ID) from bill;"):
                    num.append(i[0])

                value = num

            elif str(args[0]) == 'zcyl_zzc':
                # 总支出金额
                data = self.sql.execute("select SUM(JE) from BILL where SZ == '支出';")

                num = []
                for i in data:
                    num.append(i[0])

                value = num[0]

            elif str(args[0]) == 'zcyl_zsr':
                # 总收入金额
                data = self.sql.execute("select SUM(JE) from BILL where SZ == '收入';")

                num = []
                for i in data:
                    num.append(i[0])

                value = num[0]

            elif str(args[0]) == 'zcyl_dbzgzc':
                # 单笔最高支出
                data = self.sql.execute("select max(JE) from bill where SZ == '支出';")

                num = []
                for i in data:
                    num.append(i[0])

                value = num[0]

            elif str(args[0]) == 'zcyl_dbzgsr':
                # 单笔最高收入
                data = self.sql.execute("select max(JE) from bill where SZ == '收入';")

                num = []
                for i in data:
                    num.append(i[0])

                value = num[0]

            elif str(args[0]) == 'zcyl_dbzgzcbfb':
                # 单笔最高支出百分比
                data = self.sql.execute("select((select max(JE) from bill where SZ == '支出') / (select SUM(JE) from BILL where SZ == '支出'));")

                num = []
                for i in data:
                    # 小数转换位百分比
                    xs = "%.2f%%" % (i[0] * 100)
                    num.append(xs)

                value = num[0]

            elif str(args[0]) == 'zcyl_dbzgsrbfb':
                # 单笔最高收入百分比
                data = self.sql.execute("select((select max(JE) from bill where SZ == '收入') / (select SUM(JE) from BILL where SZ == '收入'));")

                num = []
                for i in data:
                    # 小数转换位百分比
                    xs = "%.2f%%" % (i[0] * 100)
                    num.append(xs)

                value = num[0]

            elif str(args[0]) == 'zcyl_ms':
                # 消费分类 - 美食
                data = self.sql.execute("select JYDF from BILL where NOT JYDF == '/';")

                num = []
                for i in data:
                    num.append(i[0])

                catediff = CATENAME(num).cateDiff()
                value.append(len(catediff))

            elif str(args[0]) == 'zcyl_jt':
                # 消费分类 - 交通
                data = self.sql.execute("select JYDF from BILL where NOT JYDF == '/';")

                num = []
                for i in data:
                    num.append(i[0])

                jtgjDiff = CITYNAME(num).jtgjDiff()
                value.append(len(jtgjDiff))

            elif str(args[0]) == 'zcyl_yl':
                # 消费分类 - 娱乐
                data = self.sql.execute("select JYDF from BILL where NOT JYDF == '/';")

                num = []
                for i in data:
                    num.append(i[0])

                yuleDiff = CATENAME(num).yuleDiff()
                value.append(len(yuleDiff))

            elif str(args[0]) == 'zcyl_sh':
                # 消费分类 - 生活
                data = self.sql.execute("select JYDF from BILL where NOT JYDF == '/';")

                num = []
                for i in data:
                    num.append(i[0])

                shbkDiff = CITYNAME(num).shbkDiff()
                value.append(len(shbkDiff))

            elif str(args[0]) == 'zcyl_dzcp':
                # 消费分类 - 电子产品
                data = self.sql.execute("select JYDF from BILL where NOT JYDF == '/';")

                num = []
                for i in data:
                    num.append(i[0])

                dzcpDiff = CITYNAME(num).dzcpDiff()
                value.append(len(dzcpDiff))

            elif str(args[0]) == 'zcyl_rq':
                # 近一周消费 - 日期
                data = self.sql.execute("select strftime('%m-%d',JYSJ) from BILL group by strftime('%m-%d',JYSJ) ORDER BY strftime('%m-%d',JYSJ) desc limit 7;")

                num = []
                for i in data:
                    num.append(i[0])

                value = num

            elif str(args[0]) == 'zcyl_je':
                # 近一周消费 - 金额
                data = self.sql.execute("select sum(JE) from BILL group by strftime('%m-%d',JYSJ) ORDER BY strftime('%m-%d',JYSJ) desc limit 7;")

                num = []
                for i in data:
                    num.append(i[0])

                value = num

            elif str(args[0]) == 'zcyl_zxf':
                # 两周高低消费对比 - 总消费

                zgxf = []  # 最高消费周
                zdxf = []    # 最低消费周 列表
                sumxf = []  # 总数据

                # 总数据
                for i in self.sql.execute("select strftime('%Y-%m-%d',JYSJ), strftime('%W',JYSJ), SUM(JE)from bill GROUP by strftime('%m-%d',JYSJ);"):
                    sumxf.append([i[0], i[1], i[2]])

                # 最高消费周
                for i in self.sql.execute("select count(distinct strftime('%Y-%m-%d',JYSJ)), strftime('%W',JYSJ), SUM(JE) from bill GROUP by strftime('%W',JYSJ) ORDER BY SUM(JE) desc limit 1;"):
                    zgxf.append(i[1])

                # 最低消费周
                for i in self.sql.execute("select count(distinct strftime('%Y-%m-%d',JYSJ)), strftime('%W',JYSJ), SUM(JE) from bill GROUP by strftime('%W',JYSJ) ORDER BY SUM(JE);"):
                    zdxf.append([i[0], i[1]])

                # 求最低消费周
                zdxf_new = []

                for i in zdxf:
                    if i[0] >= 4:
                        zdxf_new.append(i[1])
                        break

                count_num = analyseTools.weekly_thing_list(zgxf, zdxf_new, sumxf)

                value = count_num

            elif str(args[0]) == 'zcyl_xftop10':
                # TOP10 消费清单
                # 商品 金额 交易时间 当前状态 支付方式

                num = []
                count = 1
                for i in self.sql.execute("select SP, JE, JYSJ, DQZT, ZFFS from bill ORDER BY JE DESC limit 10;"):
                    num.append([count, i[0], i[1], i[2], i[3], i[4]])
                    count += 1

                value = num

            elif str(args[0]) == 'xfzs_bnxffl':
                # 半年消费分类
                # -- 获取所有月份
                month = []
                for i in self.sql.execute("select strftime('%m',JYSJ) from bill GROUP BY strftime('%m',JYSJ);"):
                    month.append(i[0])

                # -- 获取 金额 交易对方 月份
                data = []
                for i in self.sql.execute("select JE, JYDF, strftime('%m',JYSJ) from bill where NOT JYDF == '/';"):
                    data.append([i[0], i[1], i[2]])

                monthList, get_month = analyseTools.get_consume_classify(month, data)

                # 返回半年月份列表，获取当前月 [美食$ 交通$ 娱乐$ 生活$ 电子产品$] 金额
                return monthList, get_month


            elif str(args[0]) == 'xfzs_xfzgyzsz':

                # 消费最高一周收支记录

                zgxfsr = []  # 最高消费收入
                zgxfzc = []  # 最高消费支出

                # 最高消费收入
                for i in self.sql.execute("select strftime('%w',JYSJ),sum(JE)  from bill where strftime('%W',JYSJ) == (select strftime('%W',JYSJ) from bill GROUP by strftime('%W',JYSJ) ORDER BY SUM(JE) desc limit 1) and NOT SZ == '/' and SZ =='收入' GROUP BY strftime('%Y-%m-%d',JYSJ);"):
                    zgxfsr.append([i[0], i[1]])

                # 最高消费支出
                for i in self.sql.execute("select strftime('%w',JYSJ),sum(JE)  from bill where strftime('%W',JYSJ) == (select strftime('%W',JYSJ) from bill GROUP by strftime('%W',JYSJ) ORDER BY SUM(JE) desc limit 1) and NOT SZ == '/' and SZ =='支出' GROUP BY strftime('%Y-%m-%d',JYSJ);"):
                    zgxfzc.append([i[0], i[1]])

                pay, income = analyseTools.get_xfzgyzsz(zgxfzc, zgxfsr)

                return pay, income

            elif str(args[0]) == 'xfzs_qngysz':
                # 全年各月收支记录
                # -- 获取所有月份
                year_month_pay = []
                for i in self.sql.execute("select strftime('%m',JYSJ),sum(JE)  from bill where NOT SZ == '/' and SZ =='支出' GROUP BY strftime('%m',JYSJ);"):
                    year_month_pay.append([i[0], i[1]])

                # -- 获取 金额 交易对方 月份
                year_month_income = []
                for i in self.sql.execute("select strftime('%m',JYSJ),sum(JE)  from bill where NOT SZ == '/' and SZ =='收入' GROUP BY strftime('%m',JYSJ);"):
                    year_month_income.append([i[0], i[1]])

                maxvalue, monthpay_list, monthincome_list = analyseTools.get_year_month_sz(year_month_pay, year_month_income)

                return maxvalue, monthpay_list, monthincome_list

            elif str(args[0]) == 'xffb_jcxfsp':
                # 经常消费商铺
                data = self.sql.execute("select JYDF from BILL where NOT JYDF == '/';")

                num = []
                for i in data:
                    num.append(i[0])

                catediff = CATENAME(num).cateDiff()

                jcxfsp_list = analyseTools.get_xffb_jcxfsp(catediff, num)

                return jcxfsp_list

            elif str(args[0]) == 'xffb_rcsh':
                # 日常生活
                # 分类
                # 滴滴 地铁 外卖 医院 垃圾食品 飞机 酒店 购物 美食 其他
                data = self.sql.execute("select (select count(JYDF) from bill where JYDF LIKE '%滴滴%'),(select count(SP) from bill where SP LIKE '%地铁%' or JYDF LIKE '%北京轨道交通%'),(select count(SP) from bill where SP LIKE '%外卖%' or JYDF LIKE '%上海拉扎斯信息科技有限公司%'),(select count(SP) from bill where SP LIKE '%医院%' or JYDF LIKE '%医院%' or JYDF LIKE '%门诊%'),(select count(SP) from bill where  JYDF LIKE '%麦当劳%' or JYDF LIKE '%肯德基%' or JYDF LIKE '%辣条%'),(select COUNT(SP) from BILL where SP LIKE '%机票%' or SP LIKE '%飞机%' or SP LIKE '%航空%'),(select COUNT(SP) from bill where SP LIKE '%酒店%' or JYDF LIKE '%酒店%' or SP LIKE '%宾馆%' or JYDF LIKE '%宾馆%'),(select count(SP) from bill where SP LIKE '%商场%' or JYDF LIKE '%商店%' or JYDF LIKE '%超市%' or JYDF LIKE '%便利店%'),(select count(SP) from bill where SP LIKE '%饭店%' or JYDF LIKE '%小吃%' or JYDF LIKE '%美食%' or SP LIKE '%面%' or SP LIKE '%饭%'),(select count(SP) from bill where NOT JYDF LIKE '%滴滴%' AND NOT SP LIKE '%地铁%' AND NOT JYDF LIKE '%北京轨道交通%' AND NOT SP LIKE '%外卖%' AND NOT JYDF LIKE '%上海拉扎斯信息科技有限公司%' AND NOT SP LIKE '%医院%' AND NOT JYDF LIKE '%医院%' AND NOT JYDF LIKE '%门诊%' AND NOT JYDF LIKE '%麦当劳%' AND NOT JYDF LIKE '%肯德基%' AND NOT JYDF LIKE '%辣条%' AND NOT SP LIKE '%机票%' AND NOT SP LIKE '%飞机%' AND NOT SP LIKE '%航空%' AND NOT SP LIKE '%酒店%' AND NOT JYDF LIKE '%酒店%' AND NOT SP LIKE '%宾馆%' AND NOT JYDF LIKE '%宾馆%' AND NOT SP LIKE '%商场%' AND NOT JYDF LIKE '%商店%' AND NOT JYDF LIKE '%超市%' AND NOT JYDF LIKE '%便利店%' AND NOT SP LIKE '%饭店%' AND NOT JYDF LIKE '%小吃%' AND NOT JYDF LIKE '%美食%' AND NOT SP LIKE '%面%' AND NOT SP LIKE '%饭%');")

                num = []
                for i in data:
                    for k in i:
                        num.append(k)

                return num

            elif str(args[0]) == 'xffb_xfqy':
                # 消费分布
                # 消费区域

                data = self.sql.execute("select JYDF from bill where NOT JYDF == '/' and  JYDF NOT like '%上海拉扎斯信息科技有限公司%' and  JYDF NOT like '%银行%' and  JYDF NOT like '%北京轨道交通%' and  JYDF NOT like '%携程%' and  JYDF NOT like '%手机充值%' and  JYDF NOT like '%滴滴%' group by JYDF ORDER BY count(JYDF) DESC;")

                num = []
                for i in data:
                    num.append(i[0])

                citydiff = CITYNAME(num).cityDiff()
                xfqy_city = analyseTools.get_xffb_xfqy(citydiff)

                # [[6, '北京'], [4, '阜阳'], [1, '恩平'], [0, ''], [0, '']]
                return xfqy_city

            elif str(args[0]) == 'xffb_qdqlnl':
                # 消费分布
                # 钱都去了哪里

                data = self.sql.execute("select JYDF, COUNT(JYDF) from BILL where NOT JYDF == '/' group BY JYDF order by COUNT(JYDF) DESC limit 8;")

                num = []
                for i in data:
                    num.append([i[0], i[1]])

                return num


            else:
                print('Input Error!')

        except IndexError:
            pass

        return value


    def queryBill(self, *args):

        '''

        微信账单

        1. 共计吃饭消费                       (wxzd_cfxf)
        2. 交通出行消费                       (wxzd_jtxf)
        3. 预测生日                           (wxzd_ycsr)
        4. 计天,消费次,均消费,均每消费        (wxzd_tcxx)
        5. 最高消费的一天                     (wxzd_zgxf)
        6. 扫二维码付款,商户消费              (wxzd_ewmsh)
        7. 账单至少消费多少钱                 (wxzd_zdxf)
        8. 账单时间格式                       (wxzd_zdsjgs)
        9. 微信账单 称号 随机数               (wxzd_chsjs)
        10. 合计 支出金额 收入金额 总计流水   (wxzd_zcsrzj)
        11. 会员等级                          (wxzd_hydj)
        12. 获取当前时间                      (wxzd_time)
        13. 微信账单 访问第几位用户 流水帐号  (wxzd_fwls)
        14. 微信账单 微信昵称                 (wxzd_wxnc)


        :param args:
        :return:
        '''



        value = []

        try:

            if str(args[0]) == 'wxzd_cfxf':

                # 共计吃饭消费

                data = self.sql.execute("select SUM(JE) from bill where SP LIKE '%饭店%' or JYDF LIKE '%小吃%' or "
                                        "JYDF LIKE '%美食%' or SP LIKE '%面%' or SP LIKE '%饭%';")

                num = []
                for i in data:
                    num.append(i[0])

                return num

            elif str(args[0]) == 'wxzd_jtxf':

                # 交通出行消费

                data = self.sql.execute("select SUM(JE) from bill where JYDF  LIKE '%滴滴%' or SP LIKE '%地铁%' or JYDF "
                                        "LIKE '%北京轨道交通%' or JYDF LIKE '%车%' or JYDF LIKE '%加油%' or SP LIKE '%加油%';")

                num = []
                for i in data:
                    num.append(i[0])

                return num

            elif str(args[0]) == 'wxzd_ycsr':

                # 预测生日

                data = self.sql.execute("select strftime('%Y-%m-%d',JYSJ) from bill where JYDF LIKE '%生日%' or JYDF"
                                        " LIKE '%蛋糕%' or SP LIKE '%生日%' or SP LIKE '%蛋糕%' LIMIT 1;")

                num = []
                for i in data:
                    num.append(i[0])

                return num

            elif str(args[0]) == 'wxzd_tcxx':

                # 共计200天, 共消费600次, 平均每天至少消费7次, 平均每次消费20元

                data = self.sql.execute("SELECT (select count(distinct strftime('%Y-%m-%d',JYSJ)) from bill),(select "
                                        "count(SP) from BILL where NOT JYDF == '/' or NOT SP == '/' or NOT SZ == '收入'),"
                                        " (select((select count(SP) from BILL where NOT JYDF == '/' or NOT SP == '/')"
                                        " / (select count(distinct strftime('%Y-%m-%d',JYSJ)) from bill))),"
                                        " (select(((SELECT SUM(JE) from BILL WHERE SZ == '支出' or SZ== '/') / "
                                        "(select count(SP) from BILL where NOT JYDF == '/' or NOT SP == '/' "
                                        "or NOT SZ == '收入')) / (select((select count(SP) from BILL where NOT "
                                        "JYDF == '/' or NOT SP == '/') / (select count(distinct "
                                        "strftime('%Y-%m-%d',JYSJ)) from bill)))));")

                num = []        # [[85, 332, 3, 34.1]]
                for i in data:
                    num.append([i[0], i[1], i[2], round(i[3], 2)])

                return num

            elif str(args[0]) == 'wxzd_zgxf':

                # 最高消费的一天

                data = self.sql.execute("select strftime('%Y-%m-%d',JYSJ) from BILL GROUP BY strftime('%Y-%m-%d',JYSJ)"
                                        " ORDER BY SUM(JE) DESC limit 1;")

                num = []        #
                for i in data:
                    num.append(i[0])

                return num

            elif str(args[0]) == 'wxzd_ewmsh':

                # 扫二维码付款, 商户消费

                data = self.sql.execute("SELECT (SELECT SUM(JE) from BILL WHERE JYLX == '扫二维码付款'), (SELECT SUM(JE) "
                                        "from BILL WHERE JYLX == '商户消费');")

                num = []
                for i in data:
                    num.append([i[0], i[1]])

                return num

            elif str(args[0]) == 'wxzd_zdxf':

                # 账单至少消费多少钱

                data = self.sql.execute("SELECT SUM(JE) FROM BILL where NOT SP == '/';")

                num = []
                for i in data:
                    num.append(round(i[0], 2))

                return num

            elif str(args[0]) == 'wxzd_zdsjgs':

                # 账单时间格式

                data = []
                for i in self.sql.execute("select min(distinct strftime('%Y/%m/%d',JYSJ)) from bill;"):
                    data.append(i)

                for i in self.sql.execute("select max(distinct strftime('%Y/%m/%d',JYSJ)) from bill;"):
                    data.append(i)

                num = []
                for i in data:
                    num.append(i[0])

                return num

            elif str(args[0]) == 'wxzd_chsjs':

                # 微信账单 称号 随机数
                data = analyseTools.get_random_values()

                return data

            elif str(args[0]) == 'wxzd_zcsrzj':

                # 合计 支出金额 收入金额 总计流水

                data = self.sql.execute("SELECT (SELECT SUM(JE) from BILL WHERE SZ == '支出'),(SELECT SUM(JE) from "
                                        "BILL WHERE SZ == '收入'), (SELECT SUM(JE) from BILL);")

                num = []            # [[19125.49, 1209.18, 35174.27]]
                for i in data:
                    num.append([round(i[0], 2), round(i[1], 2), round(i[2], 2)])

                return num

            elif str(args[0]) == 'wxzd_hydj':

                # 会员等级
                data = self.sql.execute("SELECT SUM(JE) from BILL;")

                num = []
                for i in data:
                    num.append(round(i[0], 2))

                hydj = analyseTools.get_hydj_values(num)

                return hydj


            elif str(args[0]) == 'wxzd_time':

                # 获取当前时间

                time = analyseTools.get_current_time()

                return time

            elif str(args[0]) == 'wxzd_fwls':

                # 微信账单 访问第几位用户 流水帐号
                # [4, 1000000000000000004]
                fwls = analyseTools.get_access_count()

                return fwls

            elif str(args[0]) == 'wxzd_wxnc':

                # 微信账单 微信昵称
                wxname = get_wx_name()

                return wxname

            else:
                print('Input Error!')

        except IndexError:
            pass

        return value
