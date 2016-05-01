#_*_ coding: UTF-8 _*_
__author__ = 'evan'
import time
import json
import requests
import random

from download import download_300_500
from download import get_current_300_500
from download import download_163
from login import get_xueqiu_session
from nomore_xueqiu import HEADERS
import logger


LOG = logger.get_loger()

def predict(his_day=19):
    # 19 for 20 days before. 18 for 19days before.
    history_data = download_300_500(True)
    current_point = get_current_300_500()
    early_300 = history_data[0][0] / history_data[0][19] * 100 - 100
    early_500 = history_data[1][0] / history_data[1][19] * 100 - 100
    # print(early_300, early_500)

    current_300 = current_point[0] / history_data[0][his_day] * 100 - 100
    current_500 = current_point[1] / history_data[1][his_day] * 100 - 100
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

    change_300 = current_point[0] / history_data[0][0] * 100 - 100
    change_500 = current_point[1] / history_data[1][0] * 100 - 100
    # print(change_300, change_500)

    current_time = time.strftime('%F %T',time.localtime())
    message = current_time + '''  $沪深300(SZ399300)$ $中证500(SH000905)$ 与20天前对比涨幅分别为： '''\
              + current_300 + '% , ' + current_500 + '%, 此刻轮动信号为持有：' + sign_message + '。仅供参考，最终信号以收盘时刻为准！' \
              + '\n           关注微信订阅号：touzi-abc 交易时间内获取实时二八轮动信号！'
    # LOG.warn(message)
    # print(message)
    return message
    # sess = get_xueqiu_session()
    # timestamp = str(time.time()*1000)
    # # token = sess.get('http://xueqiu.com/c/pin/session', headers=HEADERS)
    # token = sess.get('http://xueqiu.com/service/csrf?api=%2Fstatuses%2Fupdate.json&_=', headers=HEADERS)
    # LOG.warn(token)
    # token = json.loads(token.content)
    # token = str(token.get('token'))
    # LOG.warn(token)
    # body = {'status': '<p>' + message + '</p>',
    #         'session_token': token}
    # url = 'http://xueqiu.com/statuses/update.json'
    # HEADERS.update({'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    #                 'Referer': 'http://xueqiu.com/afio',
    #                 'X-Requested-With': 'XMLHttpRequest'})
    # ret = sess.post(url, data=body, headers=HEADERS)
    # print(ret)
    # LOG.warn(ret)


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
    ret_message = ''
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
                    ret_message += '{0} 大盘, 点数:{1:.2f}\n'.format(p11[i][0], balance)
                    if hold_stock == 'p2':
                        balance *= (p2[i] * 1.0 / hold_price)
                    hold_price = p1[i]
                    hold_stock = 'p1'
            else:
                # buy p2
                if hold_stock != 'p2':
                    ret_message += '{0} 小盘, 点数:{1:.2f}\n'.format(p11[i][0], balance)
                    if hold_stock == 'p1':
                        balance *= (p1[i] * 1.0 / hold_price)
                    hold_price = p2[i]
                    hold_stock = 'p2'
        elif p2_minus > threadhold:
            # buy p2
            if hold_stock != 'p2':
                ret_message += '{0} 小盘, 点数:{1:.2f}\n'.format(p11[i][0], balance)
                if hold_stock == 'p1':
                    balance *= (p1[i] * 1.0 / hold_price)
                hold_price = p2[i]
                hold_stock = 'p2'
        else:
            if hold_stock != '':
                ret_message += '{0} 空仓, 点数:{1:.2f}\n'.format(p11[i][0], balance)
            if hold_stock == 'p1':
                balance *= (p1[i] * 1.0 / hold_price)
            elif hold_stock == 'p2':
                balance *= (p2[i] * 1.0 / hold_price)
            hold_stock = ''
        # print(p1[i], p2[i], balance)
    # print(balance)
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
