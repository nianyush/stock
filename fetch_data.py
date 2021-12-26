import baostock as bs
import pandas as pd

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:' + lg.error_code)
print('login respond  error_msg:' + lg.error_msg)

codes = ['sh.000001']
with open('code2.in', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.replace('\n', '')
        codes.append(line[0:2].lower() + '.' + line[2:])
print(codes)


#### 获取历史K线数据 ####
# 详细指标参数，参见“历史行情指标参数”章节
for code in codes:
    rs = bs.query_history_k_data_plus(
        code,
        "date,code,volume,pctChg,close,high,amount,turn",
        start_date='2017-06-01',
        end_date='2021-11-30',
        frequency="d",
        adjustflag="3")  #frequency="d"取日k线，adjustflag="3"默认不复权
    print(code)
    print('query_history_k_data_plus respond error_code:' + rs.error_code)
    print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    #### 结果集输出到csv文件 ####
    result.to_csv("./data/" + code[0:2] + code[3:] + ".csv",
                  encoding="gbk",
                  index=False)
# print(result)

#### 登出系统 ####
bs.logout()