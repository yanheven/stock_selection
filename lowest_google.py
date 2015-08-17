import json

from utils import http_request


lowest_google_detail = []
def lowest_google():
    url = 'https://www.google.com.hk/finance?output=json&num=500&noIL=1&q=[%28%28exchange%20%3D%3D%20%22SHE%22' \
          '%29%20%7C%20%28exchange%20%3D%3D%20%22SHA%22%29%29%20%26%20%28price_change_52week%20%3E%3D%20-99%29%20%' \
          '26%20%28price_change_52week%20%3C%3D%20964%29%20%26%20%28high_52week%20%3E%3D%200%29%20%26%20%28high_52week' \
          '%20%3C%3D%2022599.999999999996%29%20%26%20%28last_price%20%3E%3D%200%29%20%26%20%28last_price%20%3C%3D%' \
          '2016400%29%20%26%20%28low_52week%20%3E%3D%200%29%20%26%20%28low_52week%20%3C%3D%208834%29%20%26%20%28' \
          'average_200day_price%20%3E%3D%200%29%20%26%20%28average_200day_price%20%3C%3D%20185%29]' \
          '&restype=company&ei=9MmoVdmyK4n3jAGdhIL4Cg&gl=cn&sortas=Price52WeekPercChange&desc=1'
    http_client = http_request
    codes = []
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
                change = int(float(columns[0]['value']))
            except Exception as e:
                change = 10000
            try:
                highest = float(columns[1]['value'])

            except Exception as e:
                highest = 10000
            quotelast = 1
            if quotelast !=0 and quotelast < 100:
                try:
                    low52week = float(columns[-2]['value'])
                except Exception as e:
                    low52week = 10000
                try:
                    avg_200 = float(columns[-1]['value'])
                except Exception as e:
                    avg_200 = 10000
                if low52week > 100 or highest > 500:
                    continue
                #lowest_percent = int(quotelast / low52week * 100 -100)
                #avg_200_percent = int(quotelast / avg_200 * 100 -100)
                d = {'code':code, 'L': low52week, 'H': highest, 'change_last_year': change, 'Avg': avg_200}
                lowest_google_detail.append(d)
                codes.append(code)

    print 'google lowest: ', len(set(codes))


def write_file():

    with open('lowest_google.txt','w') as fb:
        lines = json.dumps(lowest_google_detail)
        fb.writelines(lines)


if __name__ == '__main__':
    lowest_google()
    write_file()

