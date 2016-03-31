#_*_ coding: UTF-8 _*_
__author__ = 'evan'
from download import download_300_500
from download import get_current_300_500


def predict():
    history_data = download_300_500()
    current_point = get_current_300_500()
    early_300 = history_data[0][0] / history_data[0][19] * 100 - 100
    early_500 = history_data[1][0] / history_data[1][19] * 100 - 100
    print(early_300, early_500)

    current_300 = current_point[0] / history_data[0][19] * 100 - 100
    current_500 = current_point[1] / history_data[1][19] * 100 - 100
    current_300 = str(int(current_300 * 100) / 100.0)
    current_500 = str(int(current_500 * 100) / 100.0)
    print(current_300, current_500)

    change_300 = current_point[0] / history_data[0][0] * 100 - 100
    change_500 = current_point[1] / history_data[1][0] * 100 - 100
    print(change_300, change_500)

    message = '''$蛋卷斗牛二八轮动(CSI001)$ 沪深300 中证500 与20天前对比涨幅分别为： ''' + current_300 + ',' + current_500
    print(message)


if __name__ == '__main__':
    predict()
