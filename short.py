import csv
import sys
import subprocess


def get_history(day):
    url = 'http://table.finance.yahoo.com/table.csv?s=510050.ss'
    cmd = 'wget ' + url + ' -O 510050.csv'
    handle = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result_message = handle.stderr.readlines()    
    if result_message is not None and len(result_message) > 0:
        print result_message
    reader = csv.reader(open("510050.csv"))
    amount = day
    history = []
    reader.next()
    for date, openp, highp, lowp, closep, volume, adjclose in reader:
        history.append(map(lambda x: float(x), [openp, highp, lowp, closep]))
        if amount == 0:
            break
        amount -= 1
    return history

def get_suggestion():
    history = get_history(5)
    low = sorted([i for a,b,i,c in history])[0]
    high = sorted([i for a,i,b,c in history])[-1]
    mid = (high + low)/2
    percent = (high - mid)/mid*0.618
    print low, high
    print percent
    print (1-percent)*mid, (1+percent)*mid

if __name__ == '__main__':
    get_suggestion()
