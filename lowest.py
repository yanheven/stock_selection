# -*- coding:utf-8 -*-

import httplib2
import time
import json
import datetime
import re

from utils import http_request


def manager_top(bdlx):
    # bcjd=2015-07-13&ecjd=2015-07-14
    # cjd:chang day
    # bdlx:1 buy, 2 sale
    # bbdje=10&ebdje=100 range 10 thounsand
    # bzltb: percentage %%
    # titType: sort keyword,0,1:date 3:amount(10thounsand) 5:money 8:percentage
    url = "http://stockdata.stock.hexun.com/ggzjc/data/ChangeHistory.aspx?count=9999&page=1&callback=" \
          "hxbase_json5&stateType=up&titType=5"
    if bdlx == 1:
        url +='&cjd=30'
    else:
        url += '&cjd=5'
    url += "&bdlx=" + str(bdlx)
    date = datetime.date.today()
    start_date = str(date - datetime.timedelta(days=1))
    # url += '&bcjd=%s&ecjd=%s'%(start_date,start_date)
    resp, content = http_request.request(url, "GET")
    content = content.replace('\"', '')
    content = content.replace('http:', '')
    content = re.sub(r"<[^<]*>", r"", content)
    # print content
    content = re.sub(r"(,?)(\w+?)\s*?:", r"\1'\2' :", content)
    content = content.replace("'", "\"")
    result = json.loads(content[13:-1]).get('list')
    ret_list = []
    codes = []
    for i in result:
        # print i['stockName'], i['averagePrice'], i['price'], i['circulationCapitalRatio']
        price = float(i['price'])
        if price > 1000 or bdlx == 2:
            code = str(re.sub(r"[^\(]*\(", r"", i['stockName'])[:-1])
            name = i['stockName'].split('(')[0]
            d = {'code': code, 'price': i['price'], 'ratio': i['circulationCapitalRatio'], 'name': name}
            codes.append(code)
            ret_list.append(d)
    return codes, ret_list

def lowest_today():
    # time_stamp = str(int(time.time()*1000 - 999999))
    # today lowest
    url = "http://xuanguapi.eastmoney.com/Stock/JS.aspx?type=xgq&sty=xgq&token=eastmoney&c=[hqzb04]&p=1&jn=LDGsJsMh&" \
          "ps=40&s=hqzb04&st=-1&r="

    # 3 days lowest
    url3 = 'http://xuanguapi.eastmoney.com/Stock/JS.aspx?type=xgq&sty=xgq&token=eastmoney&c=[hqzb05(1|3)]&p=1&jn=' \
          'lFnifSXE&ps=40&s=hqzb05(1|3)&st=-1&r=1437009363662'

    # 5days lowest
    url5 = 'http://xuanguapi.eastmoney.com/Stock/JS.aspx?type=xgq&sty=xgq&token=eastmoney&c=[hqzb05(1|5)]&p=1&jn=' \
          'FbpVPbpk&ps=40&s=hqzb05(1|5)&st=-1&r=1437009283929'
    http_client = httplib2.Http('.cache')
    resp, content = http_client.request(url, "GET")
    result = json.loads(content[13:]).get("Results")
    date = datetime.date.today()
    code_name = []
    codes = []
    for i in result:
        i = i.encode("utf-8").split(",")
        # if "N" or "退" in i[2]:
        #     continue
        line = i[1] + " " + i[2] + "\n"
        codes.append(i[1])
        code_name.append(line)
    if not code_name:
        return False
    codes.sort(key=lambda code : int(code))
    # print codes
    with open(str(date) + ".txt","w") as fb:
        fb.writelines(code_name)
    with open(str(date) + "-code.txt","w") as fb:
        for i in codes:
            fb.writelines(i + "\n")
    return codes


def lowest_goole():
    url = "https://www.google.com.hk/finance?output=json&start=0&num=20&noIL=1&q=[%28%28exchange%20%3D%3D%20%22SHE%22%" \
          "29%20%7C%20%28exchange%20%3D%3D%20%22SHA%22%29%29%20%26%20%28market_cap%20%3E%3D%200%29%20%26%20%28" \
          "market_cap%20%3C%3D%201930000000000%29%20%26%20%28pe_ratio%20%3E%3D%200%29%20%26%20%28pe_ratio" \
          "%20%3C%3D%2025099.999999999996%29%20%26%20%28dividend_yield%20%3E%3D%200%29%20%26%20%28dividend_yield" \
          "%20%3C%3D%206.9%29%20%26%20%28price_change_52week%20%3E%3D%20-32.55%29%20%26%20%28price_change_52week" \
          "%20%3C%3D%201405%29%20%26%20%28last_price%20%3E%3D%200%29%20%26%20%28last_price%20%3C%3D%201000%29%20%26%20" \
          "%28low_52week%20%3E%3D%200%29%20%26%20%28low_52week%20%3C%3D%20100%29]&restype=company&" \
          "ei=ExKRVfmWFYmRmAGbka1o&gl=cn&sortas=Low52Week"
    http_client = httplib2.Http('.cache')
    resp, content = http_client.request(url, "GET")
    # result = json.loads(content).get("searchresults")
    print content


def check_manager_sale():
    # check manager sale, we sale

    hold = []
    with open('hold.txt', 'r') as fb:
        lines = fb.readlines()
        for i in lines:
            hold.append(i.strip('\n'))
    manager_sale , sale_dict = manager_top(2)
    should_sale = set(hold) & set(manager_sale)
    print 'Manager sales: %s' % manager_sale
    print 'My hold: %s\n' % hold
    print "Sale stock today:"
    for i in should_sale:
        print i
    print '#' * 40


def buy_lowest_manager_hold():

    # find lowest and manager increase hold

    manager_buy_codes, manager_buy_dict = manager_top(1)
    lowest_codes = lowest_today()
    best = list(set(manager_buy_codes) & set(lowest_codes))
    codes = []
    print 'Manager buy: %s' % manager_buy_codes
    print 'Lowest: %s\n' % lowest_codes
    for i in manager_buy_codes:
        if i not in codes:
            codes.append(i)
    print "Buy stock today:"
    with open('hold.txt', 'a') as fb:
        for i in codes:
            if i in best:
                # fb.write(i + '\n')
                print i
    print '#' * 40


if __name__ == "__main__":
    # s = '{"a":"是"}'
    # str = '{"Results":["2,002672,东江环保,是","2,002663,普邦园林,是","2,002237,恒邦股份,是","2,300315,' \
    #       '掌趣科技,是","1,603188,亚邦股份,是","2,000594,国恒退,是","1,601211,国泰君安,是","2,300485,赛升药业,是",' \
    #       '"2,002773,康弘药业,是","2,002772,众兴菌业,是","2,002776,柏堡龙,是","1,603117,N万林,是","1,603589,N口子窖,是",' \
    #       '"2,002769,N普路通,是","1,603116,N红蜻蜓,是","2,002771,N真视通,是","2,002775,N文科,是"],"AllCount":"17",' \
    #       '"PageCount":"1","AtPage":"1","PageSize":"40","ErrMsg":"","UpdateTime":"2015/6/29 15:15:18","TimeOut":"3ms"}'
    # new_str = json.loads(str).get("Results")
    # for i  in new_str:
    #     print(i)

    # while not lowest_today():
    #     pass
    # lowest_goole()
    buy_lowest_manager_hold()
    check_manager_sale()
    # lowest = lowest_today()
    # print len(lowest)



