from querydb import DBAPI

db = DBAPI()

'''

    微信账单 DB API 接口

'''

# 预测查询
# print(db.queryForecast('like_thing'))


# 生活类数据库接口查询测试
# print(db.queryLife('ljsp_num'))


# 生活
# print(db.queryFootmark('like_thing'))


# 消费类查询
# print(db.queryCONSUME('zwxf'))


# 前端页面测试
# print(db.queryForeEnd('zcyl_zxf'))


# 微信账单
print(db.queryBill('wxzd_wxnc'))


