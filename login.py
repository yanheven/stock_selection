#_*_ coding: UTF-8 _*_
__author__ = 'evan'
import requests

import nomore_xueqiu
import logger


LOG = logger.get_loger()
LOGIN_XUEQIU = ''
LOGIN_MINE = ''

def _login(url, body, headers):
    session = requests.session()
    session.get('http://xueqiu.com', headers=nomore_xueqiu.HEADERS)
    try:
        login_res = session.post(url, headers=headers, data=body)
        # print(login_res.content)
    except Exception as e:
        LOG.error('login Fail: %s %s' % (url, e))
        return False
    else:
        LOG.warn('login : %d FOR %s' % (login_res.status_code, url))
        return session


def get_xueqiu_session():

    url = nomore_xueqiu.LOGIN_URL
    body = nomore_xueqiu.LOGIN_BODY
    headers = nomore_xueqiu.HEADERS
    return _login(url, body, headers)