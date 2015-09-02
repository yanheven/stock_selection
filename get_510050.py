import csv

def read_csv():
    total = 0
    amount = 0
    reader = csv.reader(open("510050.csv"))
    for date, openp, highp, lowp, closep, volume, adjclose in reader:
        diff = (float(highp) - float(lowp)) / float(openp)
#        total += diff
        amount += 1
        if diff > 0.04:
            total += 1
        if amount > 410:
            break
    average = float(total)/amount
    print 'average:', average

if __name__ == '__main__':
    read_csv()
