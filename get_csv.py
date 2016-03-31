import csv

def read_csv(file_name):
    reader = csv.reader(open(file_name))
    return list(reader)


if __name__ == '__main__':
    ret_list = read_csv('399905.csv')
    ret_list = read_csv('399905.csv')
    print(ret_list[-1])
