import csv

def read_csv():
    total = 0
    amount = 0
    lows = 0
    highs = 0
    reader = csv.reader(open("510050.csv"))
    for date, openp, highp, lowp, closep, volume, adjclose in reader:
        amount += 1
        openp = float(openp)
        lowp = float(lowp)
        highp = float(highp)
        lows += (openp - lowp) / openp
        highs += (highp - openp) / openp

    lowa = lows/amount
    higha = highs / amount
    print 'lowa:', lowa, 'higha:' , higha


if __name__ == '__main__':
    read_csv()
