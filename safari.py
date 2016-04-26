__author__ = 'evan'
import requests


pre_url = 'https://www.safaribooksonline.com/library/view/openstack-in-action/9781617292163/'
mid_url = 'fig'
alt_url = '_alt'
end_rul = '.jpg'
chapters = {'a0': 41,
            '01': 8,
            '02': 19,
            '03': 16,
            '04': 18,
            '05': 7,
            '06': 14,
            '07': 7,
            '08': 4,
            '9': 6,
            '10': 2,
            '11': 18,
            '12': 10}


# def get_jpb(url):
#

for ch, total in chapters.items():
    for i in xrange(1, int(total) + 1):
        index = str(i)
        if i < 10:
            index = '0' + str(i)
        preurl = pre_url + ch + mid_url + index
        url1 = preurl + end_rul
        resp = requests.get(url1, allow_redirects=False)
        name = ch + mid_url + index + end_rul
        if resp.status_code != 200:
            url2 = preurl + alt_url + end_rul
            # print(url2)
            resp = requests.get(url2, allow_redirects=False)
            name = ch + mid_url + index + alt_url + end_rul
        with open(name, 'w') as fb:
            fb.write(resp.content)
