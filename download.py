__author__ = 'evan'
import requests
import xlrd


def download_300_500():
    url500 = 'http://115.29.204.48/webdata/Csi905Perf.xls'
    url300 = 'http://115.29.204.48/webdata/Csi300Perf.xls'
    ret_list = []
    for i in [url300, url500]:
        name = i.split('/')[-1]
        ret = requests.get(i)
        with open(name, 'w') as fb:
            fb.write(ret.content)

        data = xlrd.open_workbook(name)
        table = data.sheets()[0]
        lines = []
        for rnum in range(1,table.nrows):
            rvalue = table.row_values(rnum)[7]
            rvalue = float(rvalue)
            lines.append(rvalue)
            # print(rvalue)
        ret_list.append(lines)
    return ret_list


def get_current_300_500():
    url300 = 'http://hq.sinajs.cn/list=s_sz399300'
    url500 = 'http://hq.sinajs.cn/list=s_sh000905'
    ret_list = []
    for i in [url300, url500]:
        ret = requests.get(i)
        point = ret.content.split(',')[1]
        point = float(point)
        # print(point)
        ret_list.append(point)
    return ret_list


if __name__ == '__main__':
    print(download_300_500())
