import requests
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
    old_user = get_28()
    print(len(old_user))
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
    old_user = list(set(old_user + ids))
    print(len(old_user))
    write_28(old_user)

def gen_send(n):
    sh = '''curl 'https://im8.xueqiu.com/im-comet/v2/messages.json?user_id=6391839192' -H 'Origin: https://im8.xueqiu.com' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,en-GB;q=0.2' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36' -H 'Content-Type: application/json' -H 'Accept: */*' -H 'Referer: https://im8.xueqiu.com/proxy2.html' -H 'Cookie: s=fs311zsufz; bid=f507d90c8e6824d45daf940d93ff2766_ifffwmfh; webp=0; snbim_minify=false; xq_a_token=29471b6f61e052211fcccf4ecef5d53f462f3246; xqat=29471b6f61e052211fcccf4ecef5d53f462f3246; xq_r_token=5c8299aae4dc67c360077c6eba4b47a2a69a3954; xq_is_login=1; u=6391839192; xq_token_expire=Tue%20May%2003%202016%2013%3A33%3A28%20GMT%2B0800%20(CST); Hm_lvt_1db88642e346389874251b5a1eded6e3=1459820663; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1460093611' -H 'Connection: keep-alive' --data-binary $'{"toId":replace_me,"toGroup":false,"sequenceId":294356010,"plain":"\u8bda\u9080\u5173\u6ce8\uff08WEl\u4fe1\u8ba2\u9605\u53f7\uff1a touzi-abc \uff09\uff0c\u6bcf\u5929\u6536\u76d8\u524d\u53ca\u65f6\u63a8\u9001\u6700\u65b0\u3010\u86cb\u5377\u6597\u725b\u4e8c\u516b\u8f6e\u52a8\u3011\u4fe1\u606f\u3002"}' --compressed\n\n'''
    send_name = '28_sent.txt'
    all_user = get_28()
    sent_user = get_28(send_name)
    to_send_user = list(set(all_user) - set(sent_user))
    to_send_user = to_send_user[:n]
    sent_user += to_send_user
    write_28(sent_user, send_name)
    for i in to_send_user:
        bash = sh.replace('replace_me', i)
        print(bash)


if __name__ == '__main__':
    get_follow()



