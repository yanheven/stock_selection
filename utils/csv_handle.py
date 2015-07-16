__author__ = 'evan'
import csv

def read_csv(file_path):
    """
    read cvs and return list
    :param file_path:
    :return:
    """
    ret_list = []
    with open(file_path) as csvfile:
        reader = csv.reader(csvfile,dialect='excel')
        for row in reader:
            ret_list.append(row)
    return ret_list[1:]

# print read_csv("/home/evan/code/yanheven/stock_selection/000001.csv")