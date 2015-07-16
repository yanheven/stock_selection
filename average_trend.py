__author__ = 'evan'
from utils.csv_handle import read_csv


def day_average(list_price):
    if not list_price:
        return None
    day_amount = [0]*31
    day_prices = [0]*31
    for i in list_price:
        day = int(i[0][8:]) - 1
        day_amount[day] += 1
        day_prices[day] += float(i[6])

    max = 0
    max_index = 0
    min = 999999
    min_index = 0
    for i in range(31):
        day_prices[i] /= day_amount[i]
        if day_prices[i] > max:
            max = day_prices[i]
            max_index = i
            # print 'max :', i
        if day_prices[i] < min:
            min = day_prices[i]
            min_index = i
            # print 'min: ', i

    return 'max: ',max_index,'min: ', min_index, day_prices


def get_year(prices):
    year_list = {}
    for i in prices:
        year = str(i[0][:4])
        if not year_list.get(year):
            year_list[year] = []
        year_list[year].append(i)
    return year_list


if __name__ == '__main__':
    path_prefix = "/home/evan/code/yanheven/stock_selection/"
    file_name = ["000300.ss.csv", "399001.SZ.csv", "000001.zs.csv"]
    new_file = []
    for i in file_name:
        new_file.append(path_prefix + i)

    for i in new_file:
        prices = get_year(read_csv(i))
        print prices.keys()
        for i in range(2015, 1995, -1):
            print i, day_average(prices.get(str(i)))


        # print day_average(prices[:-100])

    # prices = read_csv(file)
    #
    # day_average(prices)

