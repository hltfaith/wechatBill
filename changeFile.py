import re
import os
import sys
import shutil

import querydb
from tool.analyseTools import get_file_md5

# 判断系统环境
if sys.platform == 'linux':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/js/charts/'
    CHART_BAK = os.path.dirname(os.path.abspath(__file__)) + '/static/chartbak/'
    UPLOADS_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/uploads/'
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + '/'
    WXDOCX_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/doc/'

else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) + '\\static\\js\\charts\\'
    CHART_BAK = os.path.dirname(os.path.abspath(__file__)) + '\\static\\chartbak\\'
    UPLOADS_DIR = os.path.dirname(os.path.abspath(__file__)) + '\\static\\uploads\\'
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + '\\'
    WXDOCX_DIR = os.path.dirname(os.path.abspath(__file__)) + '\\static\\doc\\'

def copyFile(srcfile, dstfile):
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


def reductionFile():
    '''
    还原Chart JS文件
    :return:
    '''

    chartList = ['columnarChart.js', 'indexChart.js', 'pieChart.js', 'wechatBill.md']

    # 删除Chart JS 文件
    for i in chartList:
        os.remove(BASE_DIR + i)

    # 还原Chart JS 文件
    for i in chartList:
        copyFile(CHART_BAK+i, BASE_DIR+i)

    # 删除 用户上传账单文件
    for file in os.listdir(UPLOADS_DIR):
        os.remove(UPLOADS_DIR + file)

    # 删除 wxbill.db 数据库
    try:
        os.remove(ROOT_DIR+'wxbill.db')
    except FileNotFoundError:
        pass

    # 删除 微信账单docx
    try:

        for file in os.listdir(WXDOCX_DIR):
            os.remove(WXDOCX_DIR + file)

    except FileNotFoundError:
        pass


def changeIndexFileName(oldFileName, newFileName):
    '''
    删除更改 indexChart.js 名字
    :return:
    '''

    if (os.path.exists(BASE_DIR+oldFileName)):
            os.remove(BASE_DIR + oldFileName)

    os.rename(BASE_DIR+newFileName, BASE_DIR+oldFileName)


def indexjs():

    '''
    首页 Chart 图表后台数据更改
    :return:
    '''
    db = querydb.DBAPI()

    # 消费分类
    # 美食
    zcyl_ms = db.queryForeEnd('zcyl_ms')
    # 交通
    zcyl_jt = db.queryForeEnd('zcyl_jt')
    # 娱乐
    zcyl_yl = db.queryForeEnd('zcyl_yl')
    # 生活
    zcyl_sh = db.queryForeEnd('zcyl_sh')
    # 电子产品
    zcyl_dzcp = db.queryForeEnd('zcyl_dzcp')

    # 近一周消费
    # 日期
    zcyl_rq = db.queryForeEnd('zcyl_rq')

    # 金额
    zcyl_je = db.queryForeEnd('zcyl_je')

    # 两周高低消费对比
    zcyl_lzgdxf = db.queryForeEnd('zcyl_zxf')

    # 指定原始 indexChart.js 文件md5值
    if get_file_md5('indexChart.js', 'old') == get_file_md5('indexChart.js', 'new'):

        # 消费分类 Chart
        with open(BASE_DIR + 'indexChart.js', 'r', encoding='utf-8') as f:
            a = f.readlines()

        newfile = []

        for line in a:
            if re.search("{value:100, name:'美食'},", line):
                a = line.replace("{value:100, name:'美食'},", "{value:%d, name:'美食'}," % zcyl_ms[0])
                newfile.append(a)

            elif re.search("{value:10, name:'交通'},", line):
                a = line.replace("{value:10, name:'交通'},", "{value:%d, name:'交通'}," % zcyl_jt[0])
                newfile.append(a)

            elif re.search("{value:234, name:'娱乐'},", line):
                a = line.replace("{value:234, name:'娱乐'},", "{value:%d, name:'娱乐'}," % zcyl_yl[0])
                newfile.append(a)

            elif re.search("{value:135, name:'生活'},", line):
                a = line.replace("{value:135, name:'生活'},", "{value:%d, name:'生活'}," % zcyl_sh[0])
                newfile.append(a)

            elif re.search("{value:0, name:'电子产品'}", line):
                a = line.replace("{value:0, name:'电子产品'}", "{value:%d, name:'电子产品'}" % zcyl_dzcp[0])
                newfile.append(a)
            else:
                newfile.append(line)

        # 近一周消费 Chart
        jyzxf = []
        for i in newfile:
            if re.search("'10', '20', '30', '40', '50', '60', '70'", i):
                newfile = i.replace("data : ['10', '20', '30', '40', '50', '60', '70'],", "data : ['%s', '%s', '%s', '%s', '%s', '%s', '%s']," % (zcyl_rq[0], zcyl_rq[1], zcyl_rq[2],
                              zcyl_rq[3], zcyl_rq[4], zcyl_rq[5], zcyl_rq[6]))
                jyzxf.append(newfile)

            elif re.search("10, 52, 200, 334, 390, 330, 220", i):
                newfile = i.replace("data:[10, 52, 200, 334, 390, 330, 220]", "data:[%d, %d, %d, %d, %d, %d, %d]" % (zcyl_je[0], zcyl_je[1], zcyl_je[2],
                                                                                                               zcyl_je[3], zcyl_je[4], zcyl_je[5], zcyl_je[6]))
                jyzxf.append(newfile)

            else:
                jyzxf.append(i)

        # 两周高低消费对比 Chart
        lzgdxf = []
        for i in jyzxf:
            if re.search("11, 11, 15, 13, 12, 13, 10", i):
                jyzxf = i.replace("data:[11, 11, 15, 13, 12, 13, 10],", "data:[%d, %d, %d, %d, %d, %d, %d]," % (zcyl_lzgdxf[0][0], zcyl_lzgdxf[0][1],
                                                                                                                zcyl_lzgdxf[0][2], zcyl_lzgdxf[0][3],
                                                                                                                zcyl_lzgdxf[0][4], zcyl_lzgdxf[0][5],
                                                                                                                zcyl_lzgdxf[0][6]))
                lzgdxf.append(jyzxf)

            elif re.search("1, 2, 2, 5, 3, 2, 0", i):
                jyzxf = i.replace("data:[1, 2, 2, 5, 3, 2, 0],", "data:[%d, %d, %d, %d, %d, %d, %d]," % (zcyl_lzgdxf[1][0], zcyl_lzgdxf[1][1],
                                                                                                                zcyl_lzgdxf[1][2], zcyl_lzgdxf[1][3],
                                                                                                                zcyl_lzgdxf[1][4], zcyl_lzgdxf[1][5],
                                                                                                                zcyl_lzgdxf[1][6]))
                lzgdxf.append(jyzxf)

            else:
                lzgdxf.append(i)

        f.close()

        with open(BASE_DIR + 'indexChart1.js', 'w+', encoding='utf-8') as new:

            for i in lzgdxf:
                new.write(i)

        new.close()

        changeIndexFileName('indexChart.js', 'indexChart1.js')

    else:
        print('MD5值不正确!!')


def columnarjs():
    '''
    消费支收 Chart 图表后台数据更改
    :return:
    '''

    db = querydb.DBAPI()

    # 微信红包
    # 收, 发, 收到最大金额, 发送最大金额 , 转账次数, 转最大金额, 收最大金额
    sf_redpacket_num = db.queryCONSUME('sf_redpacket_num')

    # 返回半年月份列表
    # 获取当前月 [美食$ 交通$ 娱乐$ 生活$ 电子产品$] 金额
    monthList, get_month = db.queryForeEnd('xfzs_bnxffl')

    # 消费最高一周收支记录 [0, 0, 32.01, 821, 0, 0, 0] [-41, -39, -893, -1021.9, -218.42000000000002, -2218, -145.09]
    pay, income = db.queryForeEnd('xfzs_xfzgyzsz')

    # 全年各月收支记录
    # 获取最大值，各月支出、各月收入
    maxvalue, monthpay_list, monthincome_list = db.queryForeEnd('xfzs_qngysz')

    # 指定原始 indexChart.js 文件md5值
    if get_file_md5('columnarChart.js', 'old') == get_file_md5('columnarChart.js', 'new'):

        # 消费支收 Chart
        # 微信红包
        wxhbList = []

        with open(BASE_DIR + 'columnarChart.js', 'r', encoding='utf-8') as f:
            a = f.readlines()

        for wxhb in a:
            if re.search("10, 52, 200, 334, 390, 330, 220", wxhb):
                a = wxhb.replace("data:[10, 52, 200, 334, 390, 330, 220]", "data:[%d, %d, %d, %d, %d, %d, %d]" % (sf_redpacket_num[0], sf_redpacket_num[1],
                                                                                                                  sf_redpacket_num[2], sf_redpacket_num[3],
                                                                                                                  sf_redpacket_num[4], sf_redpacket_num[5],
                                                                                                                  sf_redpacket_num[6]))
                wxhbList.append(a)

            else:
                wxhbList.append(wxhb)

        # 半年消费分类
        # 返回半年月份列表
        bnxfflList = []
        for bnxf in wxhbList:
            if re.search("'1月','2月','3月','4月','5月','6月','7月'", bnxf):
                a = bnxf.replace("data: ['1月','2月','3月','4月','5月','6月','7月']", "data: ['%s月','%s月','%s月','%s月','%s月','%s月','%s月']" % (str(monthList[0]), str(monthList[1]),
                                                                                                                        str(monthList[2]), str(monthList[3]),
                                                                                                                        str(monthList[4]), str(monthList[5]), str(monthList[6])))
                bnxfflList.append(a)

            else:
                bnxfflList.append(bnxf)

        # 获取当前月 [美食$ 交通$ 娱乐$ 生活$ 电子产品$] 金额
        getmonthList = []
        for gqdy in bnxfflList:

            # 美食
            if re.search("320, 302, 301, 334, 390, 330, 320", gqdy):
                a = gqdy.replace("data: [320, 302, 301, 334, 390, 330, 320]", "data:[%d, %d, %d, %d, %d, %d, %d]" % (get_month[0][0], get_month[0][1],
                                                                                                                     get_month[0][2], get_month[0][3],
                                                                                                                     get_month[0][4], get_month[0][5],
                                                                                                                     get_month[0][6]))
                getmonthList.append(a)

            # 交通
            elif re.search("120, 132, 101, 134, 90, 230, 210", gqdy):
                a = gqdy.replace("data: [120, 132, 101, 134, 90, 230, 210]", "data:[%d, %d, %d, %d, %d, %d, %d]" % (get_month[1][0], get_month[1][1],
                                                                                                                     get_month[1][2], get_month[1][3],
                                                                                                                     get_month[1][4], get_month[1][5],
                                                                                                                     get_month[1][6]))
                getmonthList.append(a)

            # 娱乐
            elif re.search("220, 182, 191, 234, 290, 330, 310", gqdy):
                a = gqdy.replace("data: [220, 182, 191, 234, 290, 330, 310]", "data:[%d, %d, %d, %d, %d, %d, %d]" % (get_month[2][0], get_month[2][1],
                                                                        get_month[2][2], get_month[2][3],
                                                                        get_month[2][4], get_month[2][5],
                                                                        get_month[2][6]))
                getmonthList.append(a)

            # 生活
            elif re.search("150, 212, 201, 154, 190, 330, 410", gqdy):
                a = gqdy.replace("data: [150, 212, 201, 154, 190, 330, 410]", "data:[%d, %d, %d, %d, %d, %d, %d]" % (get_month[3][0], get_month[3][1],
                                                                        get_month[3][2], get_month[3][3],
                                                                        get_month[3][4], get_month[3][5],
                                                                        get_month[3][6]))
                getmonthList.append(a)

            # 电子产品
            elif re.search("820, 832, 901, 934, 1290, 1330, 1320", gqdy):
                a = gqdy.replace("data: [820, 832, 901, 934, 1290, 1330, 1320]", "data:[%d, %d, %d, %d, %d, %d, %d]" % (get_month[4][0], get_month[4][1],
                                                                        get_month[4][2], get_month[4][3],
                                                                        get_month[4][4], get_month[4][5],
                                                                        get_month[4][6]))
                getmonthList.append(a)

            else:
                getmonthList.append(gqdy)

        # 消费最高一周收支记录
        xfzgszList = []
        for zgsz in getmonthList:

            # 支出
            if re.search("-120, -132, -101, -134, -190, -230, -210", zgsz):
                a = zgsz.replace("data:[-120, -132, -101, -134, -190, -230, -210]", "data:[%d, %d, %d, %d, %d, %d, %d]" % (pay[0], pay[1],
                                                                                                                     pay[2], pay[3],
                                                                                                                     pay[4], pay[5],
                                                                                                                     pay[6]))
                xfzgszList.append(a)

            elif re.search("320, 302, 341, 374, 390, 450, 420", zgsz):
                a = zgsz.replace("data:[320, 302, 341, 374, 390, 450, 420]", "data:[%d, %d, %d, %d, %d, %d, %d]" % (income[0], income[1],
                                                                                                                    income[2], income[3],
                                                                                                                    income[4], income[5],
                                                                                                                    income[6]))
                xfzgszList.append(a)

            else:
                xfzgszList.append(zgsz)

        # 全年各月收支记录
        qngyszList = []
        for qngy in xfzgszList:

            # 最大值
            if re.search("max: 250,", qngy):
                a = qngy.replace("max: 250,", "max: %d," % maxvalue[0])
                qngyszList.append(a)

            # 支出
            elif re.search("20, 49, 70, 32, 56, 67, 36, 22, 26, 50, 64, 33", qngy):
                a = qngy.replace("data:[20, 49, 70, 32, 56, 67, 36, 22, 26, 50, 64, 33]", "data:[%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d]" % (monthpay_list[0], monthpay_list[1],
                                                                                                                                                     monthpay_list[2], monthpay_list[3],
                                                                                                                                                     monthpay_list[4], monthpay_list[5],
                                                                                                                                                     monthpay_list[6], monthpay_list[7],
                                                                                                                                                     monthpay_list[8], monthpay_list[9],
                                                                                                                                                     monthpay_list[10], monthpay_list[11]))
                qngyszList.append(a)

            # 收入
            elif re.search("26, 59, 90, 264, 28, 707, 76, 182, 87, 88, 60, 23", qngy):
                a = qngy.replace("data:[26, 59, 90, 264, 28, 707, 76, 182, 87, 88, 60, 23]",
                                 "data:[%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d]" % (
                                     monthincome_list[0], monthincome_list[1],
                                     monthincome_list[2], monthincome_list[3],
                                     monthincome_list[4], monthincome_list[5],
                                     monthincome_list[6], monthincome_list[7],
                                     monthincome_list[8], monthincome_list[9],
                                     monthincome_list[10], monthincome_list[11]))
                qngyszList.append(a)

            else:
                qngyszList.append(qngy)


        f.close()

        with open(BASE_DIR + 'columnarChart1.js', 'w+', encoding='utf-8') as new:

            for i in qngyszList:
                new.write(i)

        new.close()

        changeIndexFileName('columnarChart.js', 'columnarChart1.js')

    else:
        print('MD5值不正确!!')


def piejs():

    '''

    消费分布 Charts

    :return:
    '''

    db = querydb.DBAPI()

    # 经常消费商铺
    xffb_jcxfsp = db.queryForeEnd('xffb_jcxfsp')

    # 日常生活
    # 滴滴 地铁 外卖 医院 垃圾食品 飞机 酒店 购物 美食 其他
    xffb_rcsh = db.queryForeEnd('xffb_rcsh')

    # 消费分布
    # 消费区域
    xffb_xfqy = db.queryForeEnd('xffb_xfqy')

    # 钱都去了哪里
    xffb_qdqlnl = db.queryForeEnd('xffb_qdqlnl')

    # 指定原始 indexChart.js 文件md5值
    if get_file_md5('pieChart.js', 'old') == get_file_md5('pieChart.js', 'new'):

        # 经常消费商铺
        jcxfspList = []

        with open(BASE_DIR + 'pieChart.js', 'r', encoding='utf-8') as f:
            a = f.readlines()

        for jcxfsp in a:

            # 商铺名称
            if re.search("'田老师红烧肉','麦当劳','肯德基','庆丰包子铺','和合谷'", jcxfsp):
                a = jcxfsp.replace("data:['田老师红烧肉','麦当劳','肯德基','庆丰包子铺','和合谷']",
                                 "data:['%s', '%s', '%s', '%s', '%s']" % (xffb_jcxfsp[0][1], xffb_jcxfsp[1][1],
                                                                xffb_jcxfsp[2][1], xffb_jcxfsp[3][1],
                                                                xffb_jcxfsp[4][1]))
                jcxfspList.append(a)

            elif re.search("value:335, name:'田老师红烧肉'", jcxfsp):
                a = jcxfsp.replace("{value:335, name:'田老师红烧肉'},", "{value:%d, name:'%s'}," % (xffb_jcxfsp[0][0], xffb_jcxfsp[0][1]))
                jcxfspList.append(a)

            elif re.search("value:310, name:'麦当劳'", jcxfsp):
                a = jcxfsp.replace("{value:310, name:'麦当劳'},", "{value:%d, name:'%s'}," % (xffb_jcxfsp[1][0], xffb_jcxfsp[1][1]))
                jcxfspList.append(a)

            elif re.search("value:234, name:'肯德基'", jcxfsp):
                a = jcxfsp.replace("{value:234, name:'肯德基'},", "{value:%d, name:'%s'}," % (xffb_jcxfsp[2][0], xffb_jcxfsp[2][1]))
                jcxfspList.append(a)

            elif re.search("value:135, name:'庆丰包子铺'", jcxfsp):
                a = jcxfsp.replace("{value:135, name:'庆丰包子铺'},", "{value:%d, name:'%s'}," % (xffb_jcxfsp[3][0], xffb_jcxfsp[3][1]))
                jcxfspList.append(a)

            elif re.search("value:1548, name:'和合谷'", jcxfsp):
                a = jcxfsp.replace("{value:1548, name:'和合谷'}", "{value:%d, name:'%s'}" % (xffb_jcxfsp[4][0], xffb_jcxfsp[4][1]))
                jcxfspList.append(a)

            else:
                jcxfspList.append(jcxfsp)

        # 日常生活
        rcshList = []

        for rcsh in jcxfspList:

            # 滴滴 地铁 外卖 医院 垃圾食品 飞机 酒店 购物 美食 其他
            # [4, 10, 10, 0, 4, 3, 1, 4, 9, 71]
            if re.search("value:335, name:'美食'", rcsh):
                a = rcsh.replace("{value:335, name:'美食', selected:true},",
                                 "{value:%d, name:'美食', selected:true}," % xffb_rcsh[8])
                rcshList.append(a)

            elif re.search("value:679, name:'垃圾食品'", rcsh):
                a = rcsh.replace("{value:679, name:'垃圾食品'},",
                                 "{value:%d, name:'垃圾食品'}," % xffb_rcsh[4])
                rcshList.append(a)

            elif re.search("value:1548, name:'外卖订单'", rcsh):
                a = rcsh.replace("{value:1548, name:'外卖订单'}",
                                 "{value:%d, name:'外卖订单'}" % xffb_rcsh[2])
                rcshList.append(a)

            elif re.search("value:335, name:'滴滴打车'", rcsh):
                a = rcsh.replace("{value:335, name:'滴滴打车'},",
                                 "{value:%d, name:'滴滴打车'}," % xffb_rcsh[0])
                rcshList.append(a)

            elif re.search("value:310, name:'乘坐地铁'", rcsh):
                a = rcsh.replace("{value:310, name:'乘坐地铁'},",
                                 "{value:%d, name:'乘坐地铁'}," % xffb_rcsh[1])
                rcshList.append(a)

            elif re.search("value:234, name:'购物'", rcsh):
                a = rcsh.replace("{value:234, name:'购物'},",
                                 "{value:%d, name:'购物'}," % xffb_rcsh[7])
                rcshList.append(a)

            elif re.search("value:135, name:'医院看病'", rcsh):
                a = rcsh.replace("{value:135, name:'医院看病'},",
                                 "{value:%d, name:'医院看病'}," % xffb_rcsh[3])
                rcshList.append(a)

            elif re.search("value:1048, name:'其他'", rcsh):
                a = rcsh.replace("{value:1048, name:'其他'},",
                                 "{value:%d, name:'其他'}," % xffb_rcsh[9])
                rcshList.append(a)

            elif re.search("value:251, name:'飞机出行'", rcsh):
                a = rcsh.replace("{value:251, name:'飞机出行'},",
                                 "{value:%d, name:'飞机出行'}," % xffb_rcsh[5])
                rcshList.append(a)

            elif re.search("value:147, name:'酒店'", rcsh):
                a = rcsh.replace("{value:147, name:'酒店'}",
                                 "{value:%d, name:'酒店'}" % xffb_rcsh[6])
                rcshList.append(a)

            else:
                rcshList.append(rcsh)


        # 消费分布
        # 消费区域

        # [[6, '北京'], [4, '阜阳'], [1, '恩平'], [0, ''], [0, '']]

        xfqyList = []
        for xfqy in rcshList:
            if re.search("'北京','上海','深圳','广州','成都'", xfqy):
                a = xfqy.replace("data: ['北京','上海','深圳','广州','成都']",
                                 "data: ['%s','%s','%s','%s','%s']" % (xffb_xfqy[0][1], xffb_xfqy[1][1],
                                                                       xffb_xfqy[2][1], xffb_xfqy[3][1], xffb_xfqy[4][1]))
                xfqyList.append(a)

            elif re.search("value:335, name:'北京'", xfqy):
                a = xfqy.replace("{value:335, name:'北京'},",
                                 "{value:%d, name:'%s'}," % (xffb_xfqy[0][0], xffb_xfqy[0][1]))
                xfqyList.append(a)

            elif re.search("value:310, name:'上海'", xfqy):
                a = xfqy.replace("{value:310, name:'上海'},",
                                 "{value:%d, name:'%s'}," % (xffb_xfqy[1][0], xffb_xfqy[1][1]))
                xfqyList.append(a)

            elif re.search("value:234, name:'深圳'", xfqy):
                a = xfqy.replace("{value:234, name:'深圳'},",
                                 "{value:%d, name:'%s'}," % (xffb_xfqy[2][0], xffb_xfqy[2][1]))
                xfqyList.append(a)

            elif re.search("value:135, name:'广州'", xfqy):
                a = xfqy.replace("{value:135, name:'广州'},",
                                 "{value:%d, name:'%s'}," % (xffb_xfqy[3][0], xffb_xfqy[3][1]))
                xfqyList.append(a)

            elif re.search("value:1548, name:'成都'", xfqy):
                a = xfqy.replace("{value:1548, name:'成都'}",
                                 "{value:%d, name:'%s'}" % (xffb_xfqy[4][0], xffb_xfqy[4][1]))
                xfqyList.append(a)

            else:
                xfqyList.append(xfqy)


        # 消费分布
        # 钱都去了哪里

        qdqlnlList = []
        for qdqlnl in xfqyList:
            if re.search("'rose','rose2','rose3','rose4','rose5','rose6','rose7','rose8'", qdqlnl):
                a = qdqlnl.replace("data:['rose','rose2','rose3','rose4','rose5','rose6','rose7','rose8']",
                                 "data:['%s','%s','%s','%s','%s','%s','%s','%s']" % (xffb_qdqlnl[0][0], xffb_qdqlnl[1][0],
                                                                                     xffb_qdqlnl[2][0], xffb_qdqlnl[3][0],
                                                                                     xffb_qdqlnl[4][0], xffb_qdqlnl[5][0],
                                                                                     xffb_qdqlnl[6][0], xffb_qdqlnl[7][0]))
                qdqlnlList.append(a)

            elif re.search("value:10, name:'rose'", qdqlnl):
                a = qdqlnl.replace("{value:10, name:'rose'},",
                                 "{value:%d, name:'%s'}," % (xffb_qdqlnl[0][1], xffb_qdqlnl[0][0]))
                qdqlnlList.append(a)

            elif re.search("value:5, name:'rose2'", qdqlnl):
                a = qdqlnl.replace("{value:5, name:'rose2'},",
                                 "{value:%d, name:'%s'}," % (xffb_qdqlnl[1][1], xffb_qdqlnl[1][0]))
                qdqlnlList.append(a)

            elif re.search("value:15, name:'rose3'", qdqlnl):
                a = qdqlnl.replace("{value:15, name:'rose3'},",
                                 "{value:%d, name:'%s'}," % (xffb_qdqlnl[2][1], xffb_qdqlnl[2][0]))
                qdqlnlList.append(a)

            elif re.search("value:25, name:'rose4'", qdqlnl):
                a = qdqlnl.replace("{value:25, name:'rose4'},",
                                 "{value:%d, name:'%s'}," % (xffb_qdqlnl[3][1], xffb_qdqlnl[3][0]))
                qdqlnlList.append(a)

            elif re.search("value:20, name:'rose5'", qdqlnl):
                a = qdqlnl.replace("{value:20, name:'rose5'},",
                                 "{value:%d, name:'%s'}," % (xffb_qdqlnl[4][1], xffb_qdqlnl[4][0]))
                qdqlnlList.append(a)

            elif re.search("value:35, name:'rose6'", qdqlnl):
                a = qdqlnl.replace("{value:35, name:'rose6'},",
                                 "{value:%d, name:'%s'}," % (xffb_qdqlnl[5][1], xffb_qdqlnl[5][0]))
                qdqlnlList.append(a)

            elif re.search("value:30, name:'rose7'", qdqlnl):
                a = qdqlnl.replace("{value:30, name:'rose7'},",
                                 "{value:%d, name:'%s'}," % (xffb_qdqlnl[6][1], xffb_qdqlnl[6][0]))
                qdqlnlList.append(a)

            elif re.search("value:40, name:'rose8'", qdqlnl):
                a = qdqlnl.replace("{value:40, name:'rose8'}",
                                 "{value:%d, name:'%s'}" % (xffb_qdqlnl[7][1], xffb_qdqlnl[7][0]))
                qdqlnlList.append(a)

            else:
                qdqlnlList.append(qdqlnl)

        f.close()

        with open(BASE_DIR + 'pieChart1.js', 'w+', encoding='utf-8') as new:

            for i in qdqlnlList:
                new.write(i)

        new.close()

        changeIndexFileName('pieChart.js', 'pieChart1.js')

    else:
        print('MD5值不正确!!')



def wxbillmd():

    '''

    微信账单页面
    :return:
    '''

    db = querydb.DBAPI()

    # 外卖订单次数
    waimai_num = db.queryLife('waimai_num')

    # 吃垃圾食品的次数
    ljsp_num = db.queryLife('ljsp_num')

    # 共计吃饭消费
    wxzd_cfxf = db.queryBill('wxzd_cfxf')

    # 最爱吃的东西
    like_thing = db.queryForecast('like_thing')

    # 交通出行消费
    wxzd_jtxf = db.queryBill('wxzd_jtxf')

    # 预测生日
    wxzd_ycsr = db.queryBill('wxzd_ycsr')

    # 早上时间段消费多少笔06:00~09:30
    morn_xf_num = db.queryCONSUME('morn_xf_num')

    # 中午时间段消费多少笔11:00~13:30
    noon_xf_num = db.queryCONSUME('noon_xf_num')

    # 晚上时间段消费多少笔18:00~24:00
    night_xf_num = db.queryCONSUME('night_xf_num')

    # 计天,消费次,均消费,均每消费        (wxzd_tcxx)
    wxzd_tcxx = db.queryBill('wxzd_tcxx')

    # 最晚的一次消费
    zwxf = db.queryCONSUME('zwxf')

    # 其中几天没有消费
    daywxf = db.queryCONSUME('daywxf')

    # 最高消费的一天
    wxzd_zgxf = db.queryBill('wxzd_zgxf')

    # 扫二维码付款, 商户消费
    wxzd_ewmsh = db.queryBill('wxzd_ewmsh')

    # 账单至少消费多少钱
    wxzd_zdxf = db.queryBill('wxzd_zdxf')

    # 账单时间格式
    wxzd_zdsjgs = db.queryBill('wxzd_zdsjgs')

    # 微信账单 称号 随机数
    wxzd_chsjs = db.queryBill('wxzd_chsjs')

    # 合计 支出金额 收入金额 总计流水
    wxzd_zcsrzj = db.queryBill('wxzd_zcsrzj')

    # 会员等级
    wxzd_hydj = db.queryBill('wxzd_hydj')

    # 获取当前时间
    wxzd_time = db.queryBill('wxzd_time')

    # 微信账单 访问第几位用户 流水帐号
    wxzd_fwls = db.queryBill('wxzd_fwls')

    # 微信账单 微信名称
    wxzd_wxnc = db.queryBill('wxzd_wxnc')


    # 指定原始 indexChart.js 文件md5值
    if get_file_md5('wechatBill.md', 'old') == get_file_md5('wechatBill.md', 'new'):


        with open(BASE_DIR + 'wechatBill.md', 'r', encoding='utf-8') as f:
            a = f.readlines()

        # 微信账单

        wxzd1List = []

        for wxzd1 in a:

            # 本月外卖订单次数
            if re.search("本月外卖订单次数高达", wxzd1):
                a = wxzd1.replace("本月外卖订单次数高达<font color=red >50 次</font>",
                                 "本月外卖订单次数高达<font color=red >%s 次</font>" % str(waimai_num[0]))
                wxzd1List.append(a)

            # 吃垃圾食品的次数
            elif re.search("年轻人你竟然吃了垃圾食品", wxzd1):
                a = wxzd1.replace("年轻人你竟然吃了垃圾食品<font color=red >20 次</font>",
                                 "年轻人你竟然吃了垃圾食品<font color=red >%s 次</font>" % str(ljsp_num[0][0]))
                wxzd1List.append(a)

            # 共计吃饭消费
            elif re.search("民以食为天,共计吃饭消费", wxzd1):
                a = wxzd1.replace("民以食为天,共计吃饭消费<font color=red >5000元</font>",
                                  "民以食为天,共计吃饭消费<font color=red >%s元</font>" % str(round(wxzd_cfxf[0], 2)))
                wxzd1List.append(a)

            # 最爱吃的东西
            elif re.search("天呐，没想到！你竟然最爱吃的是这个", wxzd1):
                a = wxzd1.replace("天呐，没想到！你竟然最爱吃的是这个：<font color=red >番茄炒鸡蛋</font>",
                                  "天呐，没想到！你竟然最爱吃的是这个：<font color=red >%s</font>" % str(like_thing[0]))
                wxzd1List.append(a)

            # 最爱吃的东西
            elif re.search("感谢您为雾霾天做出的贡献，交通出行消费", wxzd1):
                a = wxzd1.replace("感谢您为雾霾天做出的贡献，交通出行消费<font color=red >500元</font> 历史将会铭记你！",
                                  "感谢您为雾霾天做出的贡献，交通出行消费<font color=red >%s元</font> 历史将会铭记你！" %
                                  str(wxzd_jtxf[0]))
                wxzd1List.append(a)

            # 预测生日
            elif re.search("小bill 预测这一天", wxzd1):

                if len(wxzd_ycsr) == 0:
                    a = wxzd1.replace("小bill 预测这一天<font color=red > 2019-01-01 </font>是你生日，祝你生日快乐!",
                                      "小Bill 没有预测到您的生日是哪天，在此感到非常的抱歉！")
                    wxzd1List.append(a)

                else:
                    a = wxzd1.replace("小bill 预测这一天<font color=red > 2019-01-01 </font>是你生日，祝你生日快乐!",
                                      "小bill 预测这一天<font color=red > %s </font>是你生日，祝你生日快乐!" %
                                      str(wxzd_ycsr[0]))
                    wxzd1List.append(a)

            # 早上时间段消费多少笔06:00~09:30
            elif re.search("一天之季在于晨，早上时间段消费了", wxzd1):
                a = wxzd1.replace("一天之季在于晨，早上时间段消费了<font color=red > 50 </font>笔",
                                  "一天之季在于晨，早上时间段消费了<font color=red > %s </font>笔" % str(morn_xf_num[0]))
                wxzd1List.append(a)

            # 中午时间段消费多少笔11:00~13:30
            elif re.search("被称为国家GDP增长率三驾马车之一的消费，中午时间段消费", wxzd1):
                a = wxzd1.replace("被称为国家GDP增长率三驾马车之一的消费，中午时间段消费<font color=red >5000</font>笔",
                                  "被称为国家GDP增长率三驾马车之一的消费，中午时间段消费<font color=red >%s</font>笔" %
                                  str(noon_xf_num[0]))
                wxzd1List.append(a)

            # 晚上时间段消费多少笔18:00~24:00
            elif re.search("晚上时间段消费", wxzd1):
                a = wxzd1.replace("晚上时间段消费<font color=red >500</font>笔",
                                  "晚上时间段消费<font color=red >%s</font>笔" % str(night_xf_num[0]))
                wxzd1List.append(a)

            # 共计200天, 共消费600次, 平均每天至少消费7次, 平均每次消费20元
            elif re.search("次,平均每天至少消费", wxzd1):
                a = wxzd1.replace("共计<font color=red >200</font>天,共消费<font color=red >600</font>次,平均每天至少消费"
                                  "<font color=red >7</font>次,平均每次消费<font color=red >20</font>元",
                                  "共计<font color=red >%s</font>天,共消费<font color=red >%s</font>次,平均每天至少消费"
                                  "<font color=red >%s</font>次,平均每次消费<font color=red >%s</font>元" %
                                  (str(wxzd_tcxx[0][0]), str(wxzd_tcxx[0][1]), str(wxzd_tcxx[0][2]), str(wxzd_tcxx[0][3])))
                wxzd1List.append(a)

            # 消费最晚的一次
            elif re.search("年轻人不要常熬夜啦，消费最晚的一次", wxzd1):
                a = wxzd1.replace("年轻人不要常熬夜啦，消费最晚的一次<font color=red > 2019-01-09 02:22 </font>有魄力!!",
                                  "年轻人不要常熬夜啦，消费最晚的一次<font color=red > %s </font>有魄力!!" %
                                  str(zwxf[0]))
                wxzd1List.append(a)

            # 其中几天没有消费
            elif re.search("起止日期2019-01-01 至 2019-03-29 其中", wxzd1):


                if daywxf[2] == 0:
                    a = wxzd1.replace("起止日期2019-01-01 至 2019-03-29 其中<font color=red > 7 </font>天没有消费",
                                      "起止日期%s 至 %s 你居然在这段时间内<font color=red > 消费满勤 </font>!!" %
                                      (str(daywxf[0]), str(daywxf[1])))
                    wxzd1List.append(a)

                else:
                    a = wxzd1.replace("起止日期2019-01-01 至 2019-03-29 其中<font color=red > 7 </font>天没有消费",
                                      "起止日期%s 至 %s 其中<font color=red > %s </font>天没有消费" %
                                      (str(daywxf[0]), str(daywxf[1]), str(daywxf[2])))
                    wxzd1List.append(a)

            # 最高消费的一天
            elif re.search("这一天对你非常重要吧!消费已经爆表了,想想自己干了什么", wxzd1):
                a = wxzd1.replace("<font color=red >2019-01-29</font>这一天对你非常重要吧!消费已经爆表了,想想自己干了什么",
                                  "<font color=red >%s</font>这一天对你非常重要吧!消费已经爆表了,想想自己干了什么" %
                                  wxzd_zgxf[0])
                wxzd1List.append(a)

            # 扫二维码付款, 商户消费
            elif re.search("通过扫二维码付款消费", wxzd1):
                a = wxzd1.replace("通过扫二维码付款消费<font color=red > 10000 </font>元，通过商户消费 <font color=red > 美食 </font>元",
                                  "通过扫二维码付款消费<font color=red > %s </font>元，通过商户消费 <font color=red > %s </font>元" %
                                  (str(round(wxzd_ewmsh[0][0], 2)), str(round(wxzd_ewmsh[0][1], 2))))
                wxzd1List.append(a)

            # 账单至少消费多少钱
            elif re.search("总计您本次账单至少消费", wxzd1):
                a = wxzd1.replace("总计您本次账单至少消费<font color=red > 100000 </font>元，且行且珍惜",
                                  "总计您本次账单至少消费<font color=red > %s </font>元，且行且珍惜" % str(wxzd_zdxf[0]))
                wxzd1List.append(a)

            # 账单时间格式
            elif re.search("截止2019/01/01 - 2019/03/26", wxzd1):
                a = wxzd1.replace("截止2019/01/01 - 2019/03/26",
                                  "截止%s - %s" % (str(wxzd_zdsjgs[0]), str(wxzd_zdsjgs[1])))
                wxzd1List.append(a)

            # 微信账单 称号 随机数
            elif re.search("称号：消费不理智", wxzd1):
                a = wxzd1.replace("**称号：消费不理智**",
                                  "**称号：%s**" % str(wxzd_chsjs))
                wxzd1List.append(a)

            # 合计
            # 支出金额  总计流水
            elif re.search("支出金额：999,999,99", wxzd1):
                a = wxzd1.replace("支出金额：999,999,99",
                                  "支出金额：<font color=red > %s </font>￥" % str(wxzd_zcsrzj[0][0]))
                wxzd1List.append(a)

            # 收入金额
            elif re.search("收入金额：1000,000,000", wxzd1):
                a = wxzd1.replace("收入金额：1000,000,000",
                                  "收入金额：<font color=red > %s </font>￥" % str(wxzd_zcsrzj[0][1]))
                wxzd1List.append(a)

            # 收入金额
            elif re.search("总计流水：666666666", wxzd1):
                a = wxzd1.replace("总计流水：666666666￥",
                                  "总计流水：<font color=red > %s </font>￥" % str(wxzd_zcsrzj[0][2]))
                wxzd1List.append(a)

            # 会员等级
            elif re.search("会员等级：VIP客户", wxzd1):
                a = wxzd1.replace("会员等级：VIP客户",
                                  "会员等级：<font color=red > %s </font>" % str(wxzd_hydj[0]))
                wxzd1List.append(a)

            # 获取当前时间 wxzd_time
            elif re.search("2019/03/26 11:16", wxzd1):
                a = wxzd1.replace("2019/03/26 11:16",
                                  "%s" % str(wxzd_time))
                wxzd1List.append(a)

            # 微信账单
            # 流水帐号
            elif re.search("流水号：1000000000000000000", wxzd1):
                a = wxzd1.replace("流水号：1000000000000000000",
                                  "流水号：%s" % str(wxzd_fwls[1]))
                wxzd1List.append(a)

            # 访问第几位用户
            elif re.search("欢迎光临，第 1 位顾客", wxzd1):
                a = wxzd1.replace("欢迎光临，第 1 位顾客",
                                  "欢迎光临，第 %s 位顾客" % str(wxzd_fwls[0]))
                wxzd1List.append(a)

            # 访问第几位用户
            elif re.search("位客户，烦请微信转发宣传，", wxzd1):
                a = wxzd1.replace("您是本店第<font color=red > 1 </font>位客户，烦请微信转发宣传，小Bill感激不尽!!!",
                                  "您是本店第<font color=red > %s </font>位客户，烦请微信转发宣传，小Bill感激不尽!!!" % str(wxzd_fwls[0]))
                wxzd1List.append(a)

            # 微信账单 微信名称
            elif re.search("微信名称：随便", wxzd1):
                a = wxzd1.replace("微信名称：随便",
                                  "微信名称：%s" % str(wxzd_wxnc[0]))
                wxzd1List.append(a)

            else:
                wxzd1List.append(wxzd1)

        f.close()

        with open(BASE_DIR + 'wechatBill1.md', 'w+', encoding='utf-8') as new:

            for i in wxzd1List:
                new.write(i)

        new.close()

        changeIndexFileName('wechatBill.md', 'wechatBill1.md')

    else:
        print('MD5值不正确!!')



def test():
    # db = querydb.DBAPI()
    # zcyl_lzgdxf = db.queryForeEnd('zcyl_zxf')
    # print(type(zcyl_lzgdxf[0][0]))

    # monthList, get_month = db.queryForeEnd('xfzs_bnxffl')
    # print(monthList)
    # print(get_month)

    wxbillmd()

if __name__ == '__main__':

    # 还原Chart JS文件
    # reductionFile()

    # 启动 index Chart JS 数据修改
    # indexjs()
    # columnarjs()
    # piejs()
    wxbillmd()


    # 测试类
    # test()

