# coding=utf-8
import requests
import subprocess
import json
import time
from login import get_xueqiu_session
import nomore_xueqiu

url = 'http://xueqiu.com/recommend/pofriends.json?type=1&code=CSI001&start=0&count=14&_=1459486834130'


def get_28(fn='28.txt'):
    with open(fn, 'r') as fb:
        content = fb.read()
    old_user = json.loads(content)
    return old_user

def write_28(old_user, fn='28.txt'):
    contnet = json.dumps(old_user)
    with open(fn, 'w') as fb:
        fb.write(contnet)


def get_follow():
    base_url = 'http://xueqiu.com/recommend/pofriends.json?code=CSI001&type=1'
    # &start=0&count=14&_=1459486834130'
    # sess = requests.session()
    sess = get_xueqiu_session()
    ret = sess.get('http://xueqiu.com', headers=nomore_xueqiu.HEADERS)
    # old_user = get_28()
    # print(len(old_user))
    for i in range(2):
        url = base_url + '&start=' + str(i * 100) + '&count=100' + '&_=' + str(time.time())
        # url = base_url + '&start=' + str(i * 100) + '&_=' + str(time.time())
        # if i < 10:
        #     url += '&type=1'
        # else:
        #     url += '&type=1'
        ret = sess.get(url, headers=nomore_xueqiu.HEADERS)
        content = ret.content
        content = json.loads(content).get('friends')
        # content = json.loads(content)
        # if not content:
        if content:
            ids = []
            for i in content:
                ids.append(i.get('profile')[1:])
    # old_user = list(set(old_user + ids))
    # print(len(old_user))
    # write_28(old_user)
    return ids


def create_follow():
    new_user = get_follow()
    old_user = get_28()
    print(len(old_user))
    all_user = list(set(old_user + new_user))
    print(len(all_user))
    write_28(all_user)

def gen_send(n):
    sh = r'''curl 'https://im1.xueqiu.com/im-comet/v2/messages.json?user_id=6391839192' -H 'Cookie: s=1d8211yp0n; bid=f507d90c8e6824d45daf940d93ff2766_imsl96jl; snbim_minify=false; xq_a_token=29471b6f61e052211fcccf4ecef5d53f462f3246; xqat=29471b6f61e052211fcccf4ecef5d53f462f3246; xq_r_token=5c8299aae4dc67c360077c6eba4b47a2a69a3954; xq_is_login=1; u=6391839192; xq_token_expire=Wed%20May%2004%202016%2012%3A24%3A20%20GMT%2B0800%20(CST); Hm_lvt_1db88642e346389874251b5a1eded6e3=1460172914; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1460176089' -H 'Origin: https://im1.xueqiu.com' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,ja;q=0.2' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36' -H 'Content-Type: application/json' -H 'Accept: */*' -H 'cache-control: no-cache' -H 'Referer: https://im1.xueqiu.com/proxy2.html' -H 'Connection: keep-alive' --data-binary $'{"toId":'''
    sh2 = r''',"toGroup":false,"sequenceId":474889521,"plain":"\u8bda\u9080\u5173\u6ce8\uff08WEl\u4fe1\u8ba2\u9605\u53f7\uff1a touzi-abc \uff09\uff0c\u6bcf\u5929\u6536\u76d8\u524d\u53ca\u65f6\u63a8\u9001\u6700\u65b0\u3010\u86cb\u5377\u6597\u725b\u4e8c\u516b\u8f6e\u52a8\u3011\u4fe1\u606f\u3002"}' --compressed'''
    send_name = '28_sent.txt'
    all_user = get_28()
    sent_user = get_28(send_name)
    to_send_user = list(set(all_user) - set(sent_user))
    to_send_user = to_send_user[:n]
    sent_user += to_send_user
    write_28(sent_user, send_name)
    for i in to_send_user:
        bash = sh + '"' + i + '"' + sh2
        import subprocess
        print(bash+'\n')
        subprocess.call(bash, shell=True)


def create_friend(n):
    sh = r'''curl 'http://xueqiu.com/service/poster' -H 'Cookie: s=1d8211yp0n; bid=f507d90c8e6824d45daf940d93ff2766_imsl96jl; snbim_minify=false; webp=1; __utmt=1; xq_a_token=29471b6f61e052211fcccf4ecef5d53f462f3246; xqat=29471b6f61e052211fcccf4ecef5d53f462f3246; xq_r_token=5c8299aae4dc67c360077c6eba4b47a2a69a3954; xq_is_login=1; u=6391839192; xq_token_expire=Wed%20May%2004%202016%2018%3A33%3A12%20GMT%2B0800%20(CST); __utma=1.1376609423.1460172914.1460192531.1460196381.4; __utmb=1.31.10.1460196381; __utmc=1; __utmz=1.1460172914.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_1db88642e346389874251b5a1eded6e3=1460172914; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1460198032' -H 'Origin: http://xueqiu.com' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,ja;q=0.2' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: */*' -H 'cache-control: no-cache' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'Referer: http://xueqiu.com/david_freedom' --data 'url=%2Ffriendships%2Fcreate%2F'''
    sh2 = r'''.json&data%5Bremark%5D=true&data%5B_%5D=1460198051881' --compressed'''
    send_name = '28_friends.txt'
    all_user = get_28()[::-1]
    sent_user = get_28(send_name)
    to_send_user = list(set(all_user) - set(sent_user))
    to_send_user = to_send_user[:n]
    sent_user += to_send_user
    write_28(sent_user, send_name)
    for i in to_send_user:
        bash = sh + i + sh2
        print(bash+'\n')
        subprocess.call(bash, shell=True)


def send_ad():
    curl = raw_input('input curl:')
    start = int(raw_input('input start:'))
    end = int(raw_input('input end:'))
    sh1 = curl.split('"toId":')[0] + '"toId":'
    sh2 = ',"toGroup":' + curl.split(',"toGroup":')[1]
    users = get_follow()[start:end]
    for i in users:
        bash = sh1 + i + sh2
        print(bash+'\n')
        subprocess.call(bash, shell=True)


if __name__ == '__main__':
    # create_follow()
    send_ad()

