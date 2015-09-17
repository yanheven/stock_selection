import sys
if __name__ == '__main__':
    price = float(sys.argv[1])
    print [round(i*1000)/1000.0 for i in [price * 0.94, price * 0.98, price * 1.02, price * 1.06]]
