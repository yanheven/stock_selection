#_*_ coding: UTF-8 _*_
__author__ = 'evan'
import time
import json
import requests

from download import download_300_500
from download import get_current_300_500
from login import get_xueqiu_session
from nomore_xueqiu import HEADERS
import logger


LOG = logger.get_loger()

def predict():
    history_data = download_300_500(False)
    current_point = get_current_300_500()
    early_300 = history_data[0][0] / history_data[0][19] * 100 - 100
    early_500 = history_data[1][0] / history_data[1][19] * 100 - 100
    print(early_300, early_500)

    current_300 = current_point[0] / history_data[0][19] * 100 - 100
    current_500 = current_point[1] / history_data[1][19] * 100 - 100
    current_300 = str(int(current_300 * 100) / 100.0)
    current_500 = str(int(current_500 * 100) / 100.0)
    print(current_300, current_500)

    change_300 = current_point[0] / history_data[0][0] * 100 - 100
    change_500 = current_point[1] / history_data[1][0] * 100 - 100
    print(change_300, change_500)

    current_time = time.strftime('%F %T',time.localtime())
    message = current_time + ''' $蛋卷斗牛二八轮动(CSI001)$ $沪深300(SZ399300)$ $中证500(SH000905)$ 与20天前对比涨幅分别为： '''\
              + current_300 + '% , ' + current_500 + '%'
    LOG.warn(message)
    print(message)
    sess = get_xueqiu_session()
    timestamp = str(time.time()*1000)
    # token = sess.get('http://xueqiu.com/c/pin/session', headers=HEADERS)
    token = sess.get('http://xueqiu.com/service/csrf?api=%2Fstatuses%2Fupdate.json&_=', headers=HEADERS)
    LOG.warn(token)
    token = json.loads(token.content)
    token = str(token.get('token'))
    LOG.warn(token)
    body = {'status': '<p>' + message + '</p>',
            'session_token': token}
    url = 'http://xueqiu.com/statuses/update.json'
    HEADERS.update({'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                    'Referer': 'http://xueqiu.com/afio',
                    'X-Requested-With': 'XMLHttpRequest'})
    ret = sess.post(url, data=body, headers=HEADERS)
    print(ret)
    LOG.warn(ret)


if __name__ == '__main__':
    predict()
