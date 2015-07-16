__author__ = 'evan'
import datetime
import httplib2
import json
STOCK_TYPE = {'hotest' : 274, 'small' : 277, 'startup' : 276}

def baidu_index(stock_type):
    date = datetime.date.today()
    print date
    url = "http://top.baidu.com/clip?line=20&b=" + str(STOCK_TYPE[stock_type])
    http_client = httplib2.Http('.cache')
    resp, content = http_client.request(url, "GET")
    rise_list = []
    for i in content.split('\n'):
        if 'BD_DATA' in i:
            data = i.split('BD_DATA=')[1][:-2]
            res_list = json.loads(data)

            print '\n== %s most rise in first 5=='%stock_type
            for i in res_list[:5]:
                if i.get('trend') == 'rise':
                    print i['title'], i['clicks']

            print '\n==most 5=='
            for i in res_list[:5]:
                print i['title'], i['clicks']

            print '\n==most rise =='
            for i in res_list:
                if i.get('trend') == 'rise':
                    del i['tit_url']
                    del i['detail_url']
                    rise_list.append(i)
                    print i['title'], i['clicks']
            print '\n============================\n'
            break
    # date = datetime.date.today()
    # with open(str(date) + "_baidu_hot_search.txt","w") as fb:
    #     fb.writelines(json.dumps(rise_list, encoding='gbk'))

if __name__ == '__main__':
    stock_types=['hotest', 'small', 'startup']
    for i in stock_types:
        baidu_index(i)

