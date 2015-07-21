# -*- coding:utf-8 -*-

import time
import json
import datetime
import re
import urllib

from utils import http_request


MANAGER_BUY = 1
MANAGER_SALE = 2
def manager_top(bdlx, days=None):
    # bcjd=2015-07-13&ecjd=2015-07-14
    # cjd:chang day
    # bdlx:1 buy, 2 sale
    # bbdje=10&ebdje=100 range 10 thounsand
    # bzltb: percentage %%
    # titType: sort keyword,0,1:date 3:amount(10thounsand) 5:money 8:percentage
    url = "http://stockdata.stock.hexun.com/ggzjc/data/ChangeHistory.aspx?count=3000&callback=" \
          "hxbase_json5&stateType=up&titType=5"

    url += "&bdlx=" + str(bdlx)
    date = datetime.date.today()
    start_date = str(date - datetime.timedelta(days=41))
    # url += '&bcjd=%s&ecjd=%s'%(start_date,start_date)
    if days:
        url +='&cjd=' + str(days)
        # url += '&bcjd=%s&ecjd=%s'%(start_date,date)
    elif bdlx == 1:
        url +='&cjd=30'
    else:
        url += '&cjd=5'
    ret_list = []
    codes = []
    # for i in range(1, 100):
    # page = '&page=' + str(i)
    # new_url = url + page
    # print new_url
    url += '&page=1'
    print url
    resp, content = http_request.request(url, "GET")
    content = content.replace('\"', '')
    content = content.replace('http:', '')
    content = re.sub(r"<[^<]*>", r"", content)
    content = re.sub(r"(,?)(\w+?)\s*?:", r"\1'\2' :", content)
    content = content.replace("'", "\"")
    result = json.loads(content[13:-1]).get('list')
    # if not len(result):
    #     break
    for i in result:
        # print i['stockName'], i['averagePrice'], i['price'], i['circulationCapitalRatio']
        price = float(i['price'])
        if price > 10 or bdlx == 2:
            code = str(re.sub(r"[^\(]*\(", r"", i['stockName'])[:-1])
            name = i['stockName'].split('(')[0]
            d = {'code': code, 'price': i['price'], 'ratio': i['circulationCapitalRatio'], 'name': name}
            codes.append(code)
            ret_list.append(d)
    print len(codes)
    return list(set(codes)), ret_list

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

    resp, content = http_request.request(url, "GET")
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

def lowest_163():
    url = 'http://quotes.money.163.com/hs/realtimedata/service/marketIndexes.php?host=/hs/realtimedata/service/' \
          'marketIndexes.php&page=0&query=HIGH_LOW_RECENTLY.HIGH_LOW:int_-1&fields=RN,SYMBOL,CODE,NAME,TYPE,PRICE,' \
          'HIGH_LOW_RECENTLY,PERCENT&sort=PRICE&order=ASC&count=9999&type=query&callback=callback_9967058&req=51111'
    url2 ='http://quotes.money.163.com/hs/realtimedata/service/marketIndexes.php?host=/hs/realtimedata/service/' \
         'marketIndexes.php&page=1&query=HIGH_LOW_RECENTLY.HIGH_LOW:int_-1&fields=RN,SYMBOL,CODE,NAME,TYPE,PRICE,' \
         'HIGH_LOW_RECENTLY,PERCENT&sort=PRICE&order=ASC&count=25&type=query&callback=callback_1993377099&req=5112'
    resp, content = http_request.request(url, "GET")
    index = content.index('"list":[') + 7

    json_content = json.loads(content[index:-3])
    codes = []
    for i in json_content:
        code = i['SYMBOL']
        codes.append(code)
    print len(codes)
    return codes



def lowest_goole():

    url = 'https://www.google.com.hk/finance?output=json&start=0&num=900&noIL=1&q=[%28%28exchange%20%3D%3D%20%22SHE%' \
          '22%29%20%7C%20%28exchange%20%3D%3D%20%22SHA%22%29%29%20%26%20%28market_cap%20%3E%3D%200%29%20%26%20%28' \
          'market_cap%20%3C%3D%202220000000000%29%20%26%20%28pe_ratio%20%3E%3D%200%29%20%26%20%28pe_ratio' \
          '%20%3C%3D%2025099.999999999996%29%20%26%20%28dividend_yield%20%3E%3D%200%29%20%26%20%28dividend_yield' \
          '%20%3C%3D%2012.64%29%20%26%20%28price_change_52week%20%3E%3D%20-67.69%29%20%26%20%28price_change_52week' \
          '%20%3C%3D%2099%29%20%26%20%28last_price%20%3E%3D%200%29%20%26%20%28last_price%20%3C%3D%2016200.000000000002' \
          '%29%20%26%20%28low_52week%20%3E%3D%200%29%20%26%20%28low_52week%20%3C%3D%208834%29]&restype=company&' \
          'ei=WpGoVZG8BqaHjAGrzpiADw&gl=cn&sortas=Price52WeekPercChange&desc=1'

    url = 'https://www.google.com.hk/finance?output=json&noIL=1&q=[%28%28exchange%20%3D%3D%20%22SHE%2' \
          '2%29%20%7C%20%28exchange%20%3D%3D%20%22SHA%22%29%29%20%26%20%28price_change_52week%20%3E%3D%20-9999%29%2' \
          '0%26%20%28price_change_52week%20%3C%3D%2099%29%20%26%20%28last_price%20%3E%3D%200%29%20%26%20%28last_pric' \
          'e%20%3C%3D%2016200.000000000002%29%20%26%20%28low_52week%20%3E%3D%200%29%20%26%20%28low_52week%20%3C%3D%2' \
          '08834%29]&restype=company&ei=WpGoVZG8BqaHjAGrzpiADw&gl=cn&sortas=Price52WeekPercChange&desc=1&num=300&start=0'


    url = 'https://www.google.com.hk/finance?output=json&start=0&num=300&noIL=1&q=[%28%28exchange%20%3D%3D%20%22SHE%22' \
          '%29%20%7C%20%28exchange%20%3D%3D%20%22SHA%22%29%29%20%26%20%28price_change_52week%20%3E%3D%20-99%29%20%' \
          '26%20%28price_change_52week%20%3C%3D%20964%29%20%26%20%28high_52week%20%3E%3D%200%29%20%26%20%28high_52week' \
          '%20%3C%3D%2022599.999999999996%29%20%26%20%28last_price%20%3E%3D%200%29%20%26%20%28last_price%20%3C%3D%' \
          '2016400%29%20%26%20%28low_52week%20%3E%3D%200%29%20%26%20%28low_52week%20%3C%3D%208834%29]' \
          '&restype=company&ei=9MmoVdmyK4n3jAGdhIL4Cg&gl=cn&sortas=Price52WeekPercChange&desc=1'
    # encode_url = 'output=json&start=0&num=20&noIL=1&q=[((exchange == "SHE") | ' \
    #       '(exchange == "SHA")) & (price_change_52week >= -67.69) & (price_change_52week <= 964) & (high_52week >= 0)' \
    #       ' & (high_52week <= 22599.999999999996) & (last_price >= 0) & (last_price <= 16400) & (low_52week >= 0) &' \
    #       ' (low_52week <= 8834)]&restype=company&ei=9MmoVdmyK4n3jAGdhIL4Cg&gl=cn&sortas=Price52WeekPercChange'
    # print urllib.unquote(encode_url)
    #
    # url = urllib.urlencode(url)
    http_client = http_request
    codes = []
    detail = []
    # for i in range(0, 11):
    #     start = str(i)
    #     new_rul = url + '&start=' + start
    resp, content = http_client.request(url, "GET")
    lindex = content.index('"searchresults"') + 17
    rindex = content.index('"mf_searchresults"') -2
    content = content[lindex : rindex]
    json_content = json.loads(content)
    for i in json_content:
        code = i['ticker']
        columns = i['columns']
        highest = float(columns[1]['value'])
        quotelast = float(columns[-2]['value'])
        low52week = float(columns[-1]['value'])
        d = {'code':code, 'lowest': low52week, 'price': quotelast, 'highest': highest}
        # print d, int(float(quotelast - low52week)/quotelast * 100)
        detail.append(d)
        codes.append(code)

    print len(set(codes))
    return detail

def filte_lowest_from_google(detail, persent):
    lowest_codes = []
    for i in detail:
        price = float(i['price'])
        lowest = float(i['lowest'])
        if (price - lowest) < float(lowest)/persent:
            lowest_codes.append(i['code'])
    return lowest_codes



def check_manager_transaction(choice, manager_codes, lowest_detail=None):
    # choice 1 for buy, 2 for sale
    # check manager sale, we sale
    # manager_codes would be sale or buy codes

    hold_codes = []
    hold_detail = []
    with open('hold.txt', 'r') as fb:
        lines = fb.readlines()
        for i in lines:
            line = json.loads(i)
            print line['code']
            hold_codes.append(line['code'])
            hold_detail.append(line)

    should_transaction = set(hold_codes) & set(manager_codes)
    if choice == 1:
        print 'Manager buy num : %d' % len(manager_codes)
        print 'My hold: %s\n' % hold_codes
        print "buy More stock today:"
        for i in should_transaction:
            print i
        print '#' * 40 +'\n'

    else:
        print 'Manager sales num : %d' % len(manager_codes)
        print 'My hold: %s\n' % hold_codes
        for i in lowest_detail:
            code = i['code']
            for j in hold_detail:
                if code == j['code']:
                    lowest = i['lowest']
                    price_hold = j['price']
                    lowest_percent_now = int(float(i['price'] - lowest) * 100 /  lowest)
                    i['lowest_percent%_now'] = lowest_percent_now
                    profit_now = ((i['price'] / price_hold) *100 -100)
                    i['profit%_now'] = profit_now
                    print i
        print "Sale stock today:"
        for i in should_transaction:
            print i
        print '#' * 40 +'\n'



def lowest_persentage(lowest_detail, manager_buy_codes, percent, detail=None):
    lowest_codes = filte_lowest_from_google(lowest_detail, percent)
    best = list(set(manager_buy_codes) & set(lowest_codes))
    codes = []
    print 'Lowestnum: %d \n %s\n' % (len(lowest_codes), lowest_codes)
    for i in manager_buy_codes:
        if i not in codes:
            codes.append(i)
    print "Buy stock today, lowest percentage:%d" % int(100.0/percent)
    for i in codes:
        if i in best:
            print i
            for j in lowest_detail:
                    if j['code'] == i:
                        sale_price = int(j['price'] + (j['highest'] - j['lowest'])/2)
                        profit = int((sale_price / j['price'] -1)*100)
                        j['sale_price'] = sale_price
                        j['profit%'] = profit
                        print json.dumps(j)
    print '#' * 40 +'\n'


def buy_lowest_manager_hold(lowest_detail, manager_buy_codes):

    # find lowest and manager increase hold
    # lowest_detail = lowest_goole()
    # manager_buy_codes, manager_buy_dict = manager_top(1)
    for i in [10, 100.0/15, 5, 4, 100.0/30]:
        lowest_persentage(lowest_detail, manager_buy_codes, i)





def today_transaction():
    record_709 = None
    with open('709.txt', 'r') as fb:
        record_709 = [x.strip('\n') for x in fb.readlines()]

    lowest_detail = lowest_goole()
    # manager_buy_codes, manager_buy_dict = manager_top(MANAGER_BUY)
    manager_5day_buy_codes, manager_5days_buy_dict = manager_top(MANAGER_BUY, 5)
    new_manager_buy = list(set(record_709 + manager_5day_buy_codes))
    manager_sale_codes, manager_sale_dict = manager_top(MANAGER_SALE)
    buy_lowest_manager_hold(lowest_detail, new_manager_buy)
    check_manager_transaction(MANAGER_BUY, manager_5day_buy_codes)
    check_manager_transaction(MANAGER_SALE, manager_sale_codes, lowest_detail)
    with open('709.txt', 'w') as fb:
        for i in new_manager_buy:
            fb.writelines(i + '\n')

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
    today_transaction()

