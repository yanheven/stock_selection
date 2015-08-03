# -*- coding:utf-8 -*import json
import datetime
import re
import json

from utils import http_request
from utils import table_util

MANAGER_BUY = 1
MANAGER_SALE = 2
turn_over_ratio = {}
manager_buy = {}
manager_sale = {}
quantity_relative_ratio = {}
rise_top = {}
black_list = ['600418', '002554', '000960', '601808', '600597', '600280', '002341', '002229', '002478', '002088', '002407', '000670', '002116', '000510', '002167', '002421', '002635', '600890', '002652', '002078', '600393', '', '', '', '', '', '', '', '', '', '', '']
in_flow_ratio = {}
stock_size = {}
change_ratio = {}
hold_history = {}
price_now = {}
# P for profit
# Avg for average
# L for lowest
# H for highest
# MTP manager total buy price
# def read_hold(hold_codes):
#     for i in hold_codes:
#         with open()


def manager_top(bdlx, days=None):
    # bcjd=2015-07-13&ecjd=2015-07-14
    # cjd:chang day
    # bdlx:1 buy, 2 sale
    # bbdje=10&ebdje=100 range 10 thounsand
    # bzltb: percentage %%
    # titType: sort keyword,0,1:date 3:amount(10thounsand) 5:money 8:percentage
    url = "http://stockdata.stock.hexun.com/ggzjc/data/ChangeHistory.aspx?count=30000&callback=" \
          "hxbase_json5&stateType=up&titType=5"

    url += "&bdlx=" + str(bdlx)
    date = datetime.date.today()
    start_date = str(date - datetime.timedelta(days=41))
    # url += '&bcjd=%s&ecjd=%s'%(start_date,start_date)
    if days:
        url +='&cjd=' + str(days)
        # url += '&bcjd=%s&ecjd=%s'%(start_date,date)
    elif bdlx == 1:
        url +='&cjd=90'
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
            d = {'code': code, 'price': price, 'ratio': i['circulationCapitalRatio'], 'name': name}
            codes.append(code)
            ret_list.append(d)
            date = i['changeDate'][-5:]
            avgprice = float(i['averagePrice'])
            if bdlx ==1 and (not manager_buy.has_key(code) or  manager_buy[code] < avgprice):
                manager_buy[code] = avgprice
            if bdlx ==2 and (not manager_sale.has_key(code) or  manager_sale[code] > avgprice):
                manager_sale[code] = avgprice

            # elif ret_dict[code]['total_price'] < price:
            #     ret_dict[code]['total_price'] = price
            #     ret_dict[code]['date'] = date
            #     ret_dict[code]['avg'] = avgprice

    print len(codes)
    return list(set(codes)), manager_buy

def rise_east():
    url = 'http://xuanguapi.eastmoney.com/Stock/JS.aspx?type=xgq&sty=xgq&token=eastmoney&c=[hqzb11(1|5)]&p=1&jn' \
          '=AzvrOrMg&ps=40&s=hqzb11(1|5)&st=-1&r=1438007615018'
    resp, content = http_request.request(url, "GET")
    json_content = json.loads(content[13:]).get("Results")
    for i in json_content:
        detail = i.split(',')
        code = detail[1]
        fluctuation = detail[3]
        rise_top[code] = fluctuation
    print 'rise top days:', len(rise_top)


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
    # with open(str(date) + ".txt","w") as fb:
    #     fb.writelines(code_name)
    # with open(str(date) + "-code.txt","w") as fb:
    #     for i in codes:
    #         fb.writelines(i + "\n")
    # return codes

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

    url = 'https://www.google.com.hk/finance?output=json&start=50&num=1&noIL=1&q=[%28%28exchange%20%3D%3D%20%22SHE%' \
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


    url = 'https://www.google.com.hk/finance?output=json&num=500&noIL=1&q=[%28%28exchange%20%3D%3D%20%22SHE%22' \
          '%29%20%7C%20%28exchange%20%3D%3D%20%22SHA%22%29%29%20%26%20%28price_change_52week%20%3E%3D%20-99%29%20%' \
          '26%20%28price_change_52week%20%3C%3D%20964%29%20%26%20%28high_52week%20%3E%3D%200%29%20%26%20%28high_52week' \
          '%20%3C%3D%2022599.999999999996%29%20%26%20%28last_price%20%3E%3D%200%29%20%26%20%28last_price%20%3C%3D%' \
          '2016400%29%20%26%20%28low_52week%20%3E%3D%200%29%20%26%20%28low_52week%20%3C%3D%208834%29%20%26%20%28' \
          'average_200day_price%20%3E%3D%200%29%20%26%20%28average_200day_price%20%3C%3D%20185%29]' \
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
    for i in range(0, 3300, 500):
        start = str(i)
        new_rul = url + '&start=' + start
        resp, content = http_client.request(new_rul, "GET")
        lindex = content.index('"searchresults"') + 17
        rindex = content.index('"mf_searchresults"') -2
        content = content[lindex : rindex].replace('\\x26', ' ')
        # content = re.sub(r"\\x26([a-zA-Z]{2,6});", r"&\1;", content);
        json_content = json.loads(content)

        for i in json_content:
            code = i['ticker']
            if code.startswith('300'):
                continue
            columns = i['columns']
            try:
                change = float(columns[0]['value'])
            except Exception as e:
                change = 10000
            try:
                highest = float(columns[1]['value'])

            except Exception as e:
                highest = 10000
            try:
                quotelast = float(columns[-3]['value'])
            except Exception as e:
                quotelast = 10000
            if quotelast !=0:
                try:
                    low52week = float(columns[-2]['value'])
                except Exception as e:
                    low52week = 10000
                try:
                    avg_200 = float(columns[-1]['value'])
                except Exception as e:
                    avg_200 = 10000
                lowest_percent = int(quotelast / low52week * 100 -100)
                avg_200_percent = int(quotelast / avg_200 * 100 -100)
                d = {'code':code, 'L': low52week, 'price': quotelast, 'H': highest, 'change_last_year': change,
                     'L%': lowest_percent, 'Avg%': avg_200_percent, 'Avg': avg_200}
                if code == '000895':
                    d['H'] = 27.58
                # print d, int(float(quotelast - low52week)/quotelast * 100)
                detail.append(d)
                codes.append(code)

    print 'google lowest: ', len(set(codes))
    return detail

def turn_over_sina():
    url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1' \
          '&num=4000&sort=turnoverratio&asc=0&node=hs_a&symbol=&_s_r_a=init'
    resp, content = http_request.request(url, "GET")
    content = re.sub(r":(\w+?):", r"fuck", content)
    content = re.sub(r"(,?)(\w+?)\s*?:", r"\1'\2' :", content)
    content = content.replace("'", "\"")
    json_content = json.loads(content)
    for i in json_content:
        code = i['code']
        ratio = int(i['turnoverratio'])
        turn_over_ratio[code] = ratio
    print 'sina turn over ratio: ', len(turn_over_ratio)

def in_flow_sina():
    url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/MoneyFlow.ssl_bkzj_ssggzj?page=1&num=4000&sort=r0_ratio&asc=0'
    resp, content = http_request.request(url, "GET")
    content = re.sub(r"(,?)(\w+?)\s*?:", r"\1'\2' :", content)
    content = content.replace("'", "\"")
    json_content = json.loads(content)
    for i in json_content:
        code = i['symbol'][2:]
        inflow = int(float(i['r0_ratio'])*100.0)
        turn_over = int(float(i['turnover']))/100.0
        change = int(float(i['changeratio'])*1000)/10.0
        price = int(float(i['trade'])*100)/100.0
        in_flow_ratio[code] = inflow
        turn_over_ratio[code] = turn_over
        change_ratio[code] = change
        price_now[code] = price
    print 'sina turn over ratio: ', len(turn_over_ratio)
    print 'sina in flow ratio: ', len(in_flow_ratio)

def stock_size_sina():
    url = "http://money.finance.sina.com.cn/quotes_service/api/jsonp_v2.php/IO.XSRV2.CallbackList['b4VIm$HArIJ1qfKO']/Market_Center.getHQNodeDataNew?page=1&num=5000&sort=nmc&asc=0&node=hs_a"
    resp, content = http_request.request(url, "GET")
    content = content[42:-1]
    content = re.sub(r":(\w+?):", r"fuck", content)
    content = re.sub(r"(,?)(\w+?)\s*?:", r"\1'\2' :", content)
    content = content.replace("'", "\"")
    json_content = json.loads(content)
    for i in json_content:
        code = i['code']
        nmc = int(float(i['nmc'])/10000.0)
        stock_size[code] = nmc
    print 'sina stock size: ', len(stock_size)

def quantity_relative_ratio_163():
    url ='http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2' \
         'Fdiyrank.php&page=0&query=STYPE%3AEQA&fields=NO%2CSYMBOL%2CNAME%2CPRICE%2CPERCENT%2CUPDOWN%2CFIVE_MINUTE%2' \
         'COPEN%2CYESTCLOSE%2CHIGH%2CLOW%2CVOLUME%2CTURNOVER%2CHS%2CLB%2CWB%2CZF%2CPE%2CMCAP%2CTCAP%2CMFSUM%2CMFRATIO' \
         '.MFRATIO2%2CMFRATIO.MFRATIO10%2CSNAME%2CCODE%2CANNOUNMT%2CUVSNEWS&sort=LB&order=desc&count=2000&type=query'
    smal_url = 'http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2' \
         'Fdiyrank.php&page=0&query=SCSTC27_RNG%3AS&fields=NO%2CSYMBOL%2CNAME%2CPRICE%2CPERCENT%2CUPDOWN%2CFIVE_MINUTE%2' \
         'COPEN%2CYESTCLOSE%2CHIGH%2CLOW%2CVOLUME%2CTURNOVER%2CHS%2CLB%2CWB%2CZF%2CPE%2CMCAP%2CTCAP%2CMFSUM%2CMFRATIO' \
         '.MFRATIO2%2CMFRATIO.MFRATIO10%2CSNAME%2CCODE%2CANNOUNMT%2CUVSNEWS&sort=LB&order=desc&count=4000&type=query'

    resp, content = http_request.request(url, "GET")
    json_content = json.loads(content)
    stock_list = json_content.get('list')
    print json_content.get('time')
    for i in stock_list:
        code = i['CODE'][1:]
        ratio = float(str(i['LB'])[:4])
        quantity_relative_ratio[code] = ratio
    print '163 quantity_relative ratio: ', len(quantity_relative_ratio)



def filte_lowest_from_google(detail, persent=None):
    lowest_codes = []
    if persent:
        for i in detail:
            price = float(i['price'])
            lowest = float(i['L'])
            if (price - lowest) < lowest*persent/100:
                lowest_codes.append(i['code'])
    else:
        for i in detail:
            lowest_codes.append(i['code'])
    return lowest_codes

def check_reopen(manager_codes, lowest_detail):
    reopen = []
    with open('reopen.txt', 'r') as fb:
        lines = fb.readlines()
        for i in lines:
            reopen.append(i.strip('\n'))
    manager_reopen = list(set(manager_codes) & set(reopen))
    print manager_reopen
    for i in lowest_detail:
            code = i['code']
            if code in manager_reopen:
                lowest = i['L']
                price_hold = i['price']
                lowest_percent_now = int(float(i['price'] - lowest) * 100 /  lowest)
                i['lowest_percent%_now'] = lowest_percent_now
                profit_now = ((i['price'] / price_hold) *100 -100)
                i['profit%_now'] = profit_now
                print i


def check_manager_transaction(choice, lowest_detail=None):
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

    # should_transaction = set(hold_codes) & set(manager_codes)
    # if choice == 1:
    #     # print 'Manager buy num : %d' % len(manager_codes)
    #     print 'My hold: %s\n' % hold_codes
    #     print "buy More stock today:"
    #     for i in should_transaction:
    #         print i
    #     print '#' * 40 +'\n'

    # else:
    #     print 'Manager sales num : %d' % len(manager_codes)
    print 'My hold: %s\n' % hold_codes
    my_hold = []
    for i in lowest_detail:
        code = i['code']
        for j in hold_detail:
            if code == j['code']:
                lowest = i['L']
                price_hold = j['price']
                price = price_now.get(code, 10000)
                i['price'] = price
                lowest_percent_now = int(float(price - lowest) * 100 /  lowest)
                i['L%_now'] = lowest_percent_now
                profit_now = int((price / price_hold) *100 -100)
                i['P%_now'] = profit_now
                sale_price = i['price'] + (i['H'] - i['price'])/2
                profit = int((sale_price / i['price'] -1)*100)
                i['sale'] = sale_price
                i['P%'] = profit
                i['TOR'] = turn_over_ratio.get(code, 10000)
                i['LB'] = quantity_relative_ratio.get(code, 10000)
                i['IF%'] = in_flow_ratio.get(code, 10000)
                i['NMC'] = stock_size.get(code, 0)
                i['CH'] = change_ratio.get(code, 10000)
                if price / price_hold < 2:
                    my_hold.append(i)
    table_util.print_list(my_hold, ['code', 'L%', 'P%', 'L', 'price', 'H', 'sale',
                                    'Avg%', 'P%_now', 'TOR', 'LB', 'IF%','NMC', 'CH'])
    # print "Sale stock today:"
    # for i in should_transaction:
    #     print i
    print '#' * 40 +'\n'



def lowest_persentage(lowest_detail, manager_buy_codes=None, percent=None, detail=None):
    lowest_codes = filte_lowest_from_google(lowest_detail, percent)
    best = list(set(manager_buy_codes) & set(lowest_codes))
    print 'Lowestnum: %d \n' % (len(lowest_codes))
    print 'Lowest and manager buy num: %d \n' % (len(best))
    if percent:
        print "Buy stock today, lowest percentage manager buy:%d" % int(100.0/percent)
    else:
        print "Buy stock today, lowest from last year manager 5 days buy:"
    for j in lowest_detail:
        if j['code'] in best or j['code'] == '000960':
            sale_price = j['price'] + (j['H'] - j['price'])/2
            profit = int((sale_price / j['price'] -1)*100)
            j['sale_price'] = sale_price
            j['P%'] = profit
            if not percent or percent == 30:
                print json.dumps(j)
            else:
                print j['code']
    print '#' * 40 +'\n'


def lowest_manager_sort(lowest_detail):
    lowest_codes = filte_lowest_from_google(lowest_detail)
    # best = list(set(manager_buy_codes) & set(lowest_codes))
    lowest_percent_sort = sorted([i for i in lowest_detail if i['code'] in lowest_codes],key=lambda x:x['L%'])
    lowest_50 = []
    for i in lowest_percent_sort:
        sale_price = i['price'] + (i['H'] - i['price'])/2
        profit = int((sale_price / i['price'] -1)*100)
        i['sale'] = sale_price
        i['P%'] = profit
        # i['MB'] = manager_buy.get(i['code'], 10000)
        # i['MS'] = manager_sale.get(i['code'], 10000)
        # i['MTP'] = manager_5days_buy_dict[i['code']]['total_price']
        # i['date'] = manager_5days_buy_dict[i['code']]['date']
        # i['Avg'] = manager_5days_buy_dict[i['code']]['avg']
        i['TOR'] = turn_over_ratio.get(i['code'], 10000)
        i['LB'] = quantity_relative_ratio.get(i['code'], 10000)
        # i['FL'] = rise_top.get(i['code'], -10000)
        i['IF%'] = in_flow_ratio.get(i['code'], 10000)
        i['NMC'] = stock_size.get(i['code'], 0)
        i['CH'] = change_ratio.get(i['code'], 10000)
        # print json.dumps(i)
        if i['Avg'] == 10000:
            continue
        if i['L%'] < 100 and i['LB'] > 0 and i['LB']!=10000 and i['LB'] > 2.5:
            #  and i['CH'] < 5 and i['CH'] > -5:
            # and i['Avg%'] < 20:
            # and i['P%'] > 20:
            # and i['MB'] != 10000 i['TOR'] != 10000 and  :
            # and i['price'] /i['MB'] < 1.2:

            lowest_50.append(i)
        #         lowest_50.append(i)

 #   lowest_50 = sorted(lowest_50, key=lambda  x : x['L%'], reverse=True)
 #   table_util.print_list(lowest_50, ['code', 'L%', 'P%', 'price', 'Avg%', 'MB', 'MS', 'TOR', 'LB'])
    
    lowest_50 = sorted(lowest_50, key=lambda  x : x['LB'], reverse=False)[-20:]
    table_util.print_list(lowest_50, ['code', 'L%', 'P%', 'price', 'Avg%', 'TOR', 'LB', 'IF%', 'NMC', 'CH'])
    
    lowest_50 = sorted([x for x in lowest_50 if x['L%']<50], key=lambda  x : x['LB'], reverse=False)[-10:]
    table_util.print_list(lowest_50, ['code', 'L%', 'P%', 'price', 'Avg%', 'TOR', 'LB', 'IF%', 'NMC', 'CH'])



def buy_lowest_manager_hold(lowest_detail, manager_buy_codes):

    # find lowest and manager increase hold
    # lowest_detail = lowest_goole()
    # manager_buy_codes, manager_buy_dict = manager_top(1)
    for i in [10, 15, 20, 25, 30][::-1]:
        lowest_persentage(lowest_detail, manager_buy_codes, i)

def buy_lowest_manager_5day_hold(lowest_detail, manager_buy_codes):

    # find lowest and manager increase hold
    # lowest_detail = lowest_goole()
    # manager_buy_codes, manager_buy_dict = manager_top(1)
    lowest_persentage(lowest_detail, manager_buy_codes)

def bug_lowest_in_this_year(lowest_detail, percent):
    lowest_codes = filte_lowest_from_google(lowest_detail, percent)
    print 'buy lowest in this year:'
    for j in lowest_detail:
        if j['code'] in lowest_codes:
            sale_price = j['price'] + (j['H'] - j['price'])/2
            profit = int((sale_price / j['price'] -1)*100)
            j['sale_price'] = sale_price
            j['P%'] = profit
            print json.dumps(j)
    print '#' * 40 +'\n'

def today_transaction():
    #rise_east()

    lowest_detail = lowest_goole()
    # manager_buy_codes, manager_buy_dict = manager_top(MANAGER_BUY)
    # manager_buy_codes, manager_buy_dict = manager_top(MANAGER_BUY)
    #new_manager_buy = list(set(record_709 + manager_buy_codes))
    #manager_top(MANAGER_SALE, 30)
    
    stock_size_sina()
    in_flow_sina()
    #turn_over_sina()
    quantity_relative_ratio_163()
    lowest_manager_sort(lowest_detail)
    # buy_lowest_manager_hold(lowest_detail, new_manager_buy)
    # buy_lowest_manager_5day_hold(lowest_detail, manager_5day_buy_codes)
    # bug_lowest_in_this_year(lowest_detail,10)
    ##manager_sale_codes, manager_sale_dict = manager_top(MANAGER_SALE)
    #check_manager_transaction(MANAGER_BUY, manager_buy_codes)
    check_manager_transaction(MANAGER_SALE, lowest_detail)
    # check_reopen(new_manager_buy, lowest_detail)


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

