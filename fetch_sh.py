import baostock as bs
import pandas as pd
import datetime

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

#### 获取证券信息 ####

begin = datetime.date(2019,6,1)
end = datetime.date(2020,12,31)
data_list = []
for i in range((end - begin).days+1):
    day = begin + datetime.timedelta(days=i)
    

    rs = bs.query_all_stock(day=day)
    print(day)
    print('query_all_stock respond error_code:'+rs.error_code)
    print('query_all_stock respond  error_msg:'+rs.error_msg)

#### 打印结果集 ####

    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())

result = pd.DataFrame(data_list, columns=rs.fields)

#### 结果集输出到csv文件 ####   
result.to_csv("./data/sh.csv", encoding="gbk", index=False)
print(result)

#### 登出系统 ####
bs.logout()