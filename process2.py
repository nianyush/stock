import numpy as np
import datetime
import os

codes = []
with open('code2.in', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.replace('\n', '')
        codes.append(line[0:2].lower() + '.' + line[2:])


def removedot(code):
    return code[0:2] + code[3:]


def load_data(filename):
    with open('./data/' + removedot(filename), encoding='utf-8') as f:
        data = np.loadtxt(f, str, delimiter=",")

    return data[1:]


def find_idx_by_date(data, date):
    for i in range(len(data)):
        if data[i][0] == date:
            return i


def checklastKpctChg(data, szdata, index, k):
    flag = True
    for i in range(0, k ):
        szdata_idx = find_idx_by_date(szdata, data[index - i][0])
        flag &= float(data[index - i][3]) >= float(szdata[szdata_idx][3])
    # if index == 215:
    #     print(data[index][0])
    #     for i in range(3):
    #         print(data[index - i][3], szdata[index - i][3])
    return flag


def checklastKszAvg(data, szdata, index, k):
    lastKszAvg = 0
    for i in range(0, k ):
        szdata_idx = find_idx_by_date(szdata, data[index - i][0])
        lastKszAvg += float(szdata[szdata_idx][4])
    lastKszAvg /= k
    return float(szdata[index][4]) >= lastKszAvg


def checklastKcloseAvg(data, index, k):
    lastKcloseAvg = 0
    for i in range(0, k ):
        lastKcloseAvg += float(data[index - i][4])
    lastKcloseAvg /= k
    return float(data[index][4]) >= lastKcloseAvg


def getAvgVollastk(data, idx, k):
    sum = 0
    for i in range(0, k ):
        sum += int(data[idx - i][2])
    return float(sum / k)

def checktodayKpctChg(data, szdata, index):
    szdata_idx = find_idx_by_date(szdata, data[index][0])
    return float(data[index][3]) <= 3


def main():
    # files = os.listdir('./result')
    # for file in files:
    #     print(file)
    # os.rmdir('result')
    os.mkdir('result')
    szdata = load_data('sh.000001.csv')

    expect = dict()
    expect_num = dict()

    for code in codes:
        print(code)
        data = load_data(code + '.csv')
        # print(data[145]
        # print(len(data) - 145)    
        for i in range(145, len(data) - 2):
            avgVollast3 = getAvgVollastk(data, i, 3)
            avgVollast125 = getAvgVollastk(data, i, 125)

            # if i == 215:
            #     print(avgVollast3, avgVollast125)

            if avgVollast3 >= avgVollast125 and checklastKpctChg(data, szdata,i, 3) and float(data[i][3]) <= 3 and checklastKszAvg(
                    data ,szdata, i,5) and checklastKcloseAvg(data,i, 60):
                if data[i][0] in expect:
                    expect[data[i][0]] += float(data[i+1][3])
                    expect_num[data[i][0]] += 1
                else:
                    expect[data[i][0]] = float(data[i+1][3])
                    expect_num[data[i][0]] = 1
                with open('./result2/' + data[i][0] + '.csv', 'a') as f:
                    f.write(data[i][1] + ',' + data[i][3] + ',' + data[i + 1][3] + ',' + data[i + 2][3] + '\n')

    with open('./result2/expect.txt', 'w') as f:
        result = 1
        for key in sorted(expect.keys()):
            result *= 1 + (expect[key] / expect_num[key]) / 100
            f.write(key + ' ' + str(expect[key] / (1 * expect_num[key])) + ' ' + str(result) + '\n')
        f.write(str(result) + '\n')


if __name__ == '__main__':
    main()