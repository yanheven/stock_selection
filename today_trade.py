#_*_ coding: UTF-8 _*_
__author__ = 'evan'
import time
import json
import requests
import random

from download import download_300_500, get_300_500
from download import get_current_300_500
from download import download_163
from login import get_xueqiu_session
from nomore_xueqiu import HEADERS
import logger


LOG = logger.get_loger()

def predict(his_day=19):
    # 19 for 20 days before. 18 for 19days before.
    # history_data = download_300_500(True)
    all_data = download_163()
    # history_data = get_300_500()
    current_point = get_current_300_500()
    # early_300 = history_data[0][0] / history_data[0][19] * 100 - 100
    # early_500 = history_data[1][0] / history_data[1][19] * 100 - 100
    # print(early_300, early_500)
    his_300 = float(all_data[0][his_day][3])
    his_500 = float(all_data[1][his_day][3])
    current_300 = current_point[0] / his_300 * 100 - 100
    current_500 = current_point[1] / his_500 * 100 - 100
    sign_message = ''
    if current_300 >= current_500 and current_300 > 0:
        sign_message = '''沪深300'''
    elif current_300 < current_500 and current_500 > 0:
        sign_message = '''中证500'''
    else:
        sign_message = '''国债'''
    current_300 = str(int(current_300 * 100) / 100.0)
    current_500 = str(int(current_500 * 100) / 100.0)
    # print(current_300, current_500)

    # change_300 = current_point[0] / history_data[0][0] * 100 - 100
    # change_500 = current_point[1] / history_data[1][0] * 100 - 100
    # print(change_300, change_500)

    current_time = time.strftime('%F %T',time.localtime())
    # message = current_time + '''  $沪深300(SZ399300)$ $中证500(SH000905)$ 与20天前对比涨幅分别为： '''\
    #           + current_300 + '% , ' + current_500 + '%, 此刻轮动信号为持有：' + sign_message + '。仅供参考，最终信号以收盘时刻为准！' \
    #           + '\n           关注微信订阅号：touzi-abc 交易时间内获取实时二八轮动信号！'
    message = '''{0}  沪深300 中证500 ({1}, {2}) 与20天前 ({3},\
              {4}) 对比涨幅分别为：({5}%, {6}%),  此刻轮动信号为持有：{7}。仅供参考，\
              最终信号以收盘时刻为准！--内容来自http://120.26.84.164:8080/today\
              '''.format(current_time, current_point[0], current_point[1],
                          his_300, his_500, current_300, current_500, sign_message)

    # return message
    return (current_time, current_point[0], current_point[1],
            his_300, his_500, current_300, current_500, sign_message, all_data[0][his_day][0], message)


def get_predict_message(his_day=19):
    return predict(his_day)[-1]
    # data = tuple(predict(his_day)[:-1])
    # print(data)
    # message = '''{0}  $沪深300(SZ399300)$ $中证500(SH000905)$({1}, {2}) 与20天前 ({3},\
    #           {4}) 对比涨幅分别为：({5}%, {6}%),  此刻轮动信号为持有：{7}。仅供参考，\
    #           最终信号以收盘时刻为准！ 关注微信订阅号：touzi-abc 交易时间内获取实时二八轮动信号\
    #           ！'''.format(*data)
    # predict(message)
    # return message


def report():
    his = download_163()
    # p1 for big, p2 for small
    p1 = his[0][::-1]
    p2 = his[1][::-1]
    p11 = p1[:]
    p22 = p2[:]
    lenght = len(p1)
    for i in xrange(lenght):
        p1[i] = float(p1[i][3])
        p2[i] = float(p2[i][3])
    # with open('current_point.txt', 'r') as fb:
    #     balance = float(fb.read())
    balance = 100
    fixed_pro = 0.027 / 365
    fee = 0.004 / 365
    hold_stock = ''
    hold_price = 0
    # balance *= (1 + fixed_pro) ** 20
    internal = 20
    threadhold = 0.0
    ret_message = '大盘使用沪深300，小盘使用中证500，空仓时按货币基金年化2.7%收益计算。\n\n'
    for i in xrange(internal, lenght):
        if hold_stock:
            balance -= balance * fee
        else:
            balance += balance * fixed_pro
        p1_minus = p1[i] * 1.0 / p1[i-internal] - 1
        p2_minus = p2[i] * 1.0 / p2[i-internal] - 1
        if p1_minus > threadhold:
            if p1_minus > p2_minus:
                # buy p1
                if hold_stock != 'p1':
                    if hold_stock == 'p2':
                        balance *= (p2[i] * 1.0 / hold_price)
                    hold_price = p1[i]
                    hold_stock = 'p1'
                    ret_message += '{0} 大盘, 点数:{1:.2f}\n'.format(p11[i][0], balance)
            else:
                # buy p2
                if hold_stock != 'p2':
                    if hold_stock == 'p1':
                        balance *= (p1[i] * 1.0 / hold_price)
                    hold_price = p2[i]
                    hold_stock = 'p2'
                    ret_message += '{0} 小盘, 点数:{1:.2f}\n'.format(p11[i][0], balance)
        elif p2_minus > threadhold:
            # buy p2
            if hold_stock != 'p2':
                if hold_stock == 'p1':
                    balance *= (p1[i] * 1.0 / hold_price)
                hold_price = p2[i]
                hold_stock = 'p2'
                ret_message += '{0} 小盘, 点数:{1:.2f}\n'.format(p11[i][0], balance)
        else:
            if hold_stock == 'p1':
                balance *= (p1[i] * 1.0 / hold_price)
            elif hold_stock == 'p2':
                balance *= (p2[i] * 1.0 / hold_price)
            if hold_stock != '':
                ret_message += '{0} 空仓, 点数:{1:.2f}\n'.format(p11[i][0], balance)
            hold_stock = ''
        # if 1 < lenght - i <= 5:
        #     ret_message += '{0} 收盘, 点数:{1:.2f}\n'.format(p11[i][0], balance)
        if lenght - i == 6:
            if hold_stock == 'p1':
                balance_0 = balance * (p1[i] * 1.0 / hold_price)
            elif hold_stock == 'p2':
                balance_0 = balance * (p2[i] * 1.0 / hold_price)
    # print(p11)
    if hold_stock == 'p1':
        balance *= (p1[i] * 1.0 / hold_price)
    elif hold_stock == 'p2':
        balance *= (p2[i] * 1.0 / hold_price)
    ret_message += '{0} 截止, 点数:{1:.2f}\n'.format(p11[-1][0], balance)
    change = balance * 100 / balance_0 -100
    ret_message += '最后5天涨跌百分比:{0:.2f}\n'.format(change)
    # print(balance)
    return ret_message


def predict_399006(his_day=19):
    # 19 for 20 days before. 18 for 19days before.
    # history_data = download_300_500(True)
    all_data = download_163()
    # history_data = get_300_500()
    current_point = get_current_300_500()
    # early_300 = history_data[0][0] / history_data[0][19] * 100 - 100
    # early_500 = history_data[1][0] / history_data[1][19] * 100 - 100
    # print(early_300, early_500)
    his = float(all_data[2][his_day][3])
    current = current_point[2] / his * 100 - 100
    if current > 0:
        sign_message = '''创业板指'''
    else:
        sign_message = '''国债'''
    current = str(int(current * 100) / 100.0)

    current_time = time.strftime('%F %T',time.localtime())
    message = '''{0}  创业板指 ({1}) 与20天前 ({2}) 对比涨幅为：({3}%),\
              此刻轮动信号为持有：{4}。仅供参考，最终信号以收盘时刻为准！\
              --内容来自http://120.26.84.164:8080/399006\
              '''.format(current_time, current_point[2], his, current,
                         sign_message)

    # return message
    return (current_time, current_point[2],
            his, current, sign_message, all_data[2][his_day][0], message)


def get_predict_message_399006(his_day=19):
    return predict_399006(his_day)[-1]


def report_399006():
    his = download_163()
    # p1 for big, p2 for small
    p1 = his[2][::-1]
    p11 = p1[:]
    lenght = len(p1)
    for i in xrange(lenght):
        p1[i] = float(p1[i][3])
    balance = 100
    fixed_pro = 0.027 / 365
    fee = 0.004 / 365
    hold_stock = ''
    hold_price = 0
    internal = 20
    threadhold = 0.0
    ret_message = '空仓时按货币基金年化2.7%收益计算。\n\n'
    for i in xrange(internal, lenght):
        if hold_stock:
            balance -= balance * fee
        else:
            balance += balance * fixed_pro
        p1_minus = p1[i] * 1.0 / p1[i-internal] - 1
        if p1_minus > threadhold:
            # buy p1
            if hold_stock != 'p1':
                hold_price = p1[i]
                hold_stock = 'p1'
                ret_message += '{0} 创业板, 点数:{1:.2f}\n'.format(p11[i][0], balance)
        else:
            if hold_stock == 'p1':
                balance *= (p1[i] * 1.0 / hold_price)
                ret_message += '{0} 空仓中, 点数:{1:.2f}\n'.format(p11[i][0], balance)
            hold_stock = ''
        if lenght - i == 5:
            balance_0 = balance
    if hold_stock == 'p1':
        balance *= (p1[i] * 1.0 / hold_price)
    elif hold_stock == 'p2':
        balance *= (p2[i] * 1.0 / hold_price)
    ret_message += '{0} 截止时, 点数:{1:.2f}\n'.format(p11[-1][0], balance)
    change = balance * 100 / balance_0 -100
    ret_message += '最后5天涨跌百分比:{0:.2f}\n'.format(change)
    return ret_message


if __name__ == '__main__':
    # now_hour = time.strftime('%H',time.localtime())
    # if now_hour == '05':
    #     time.sleep(random.randint(1, 7200))
    # if now_hour == '09':
    #     time.sleep(random.randint(1, 300))
    # if now_hour == '14':
    #     time.sleep(random.randint(1, 500))
    # predict()
    print(report())
