import sys
if __name__ == '__main__':
    price = float(sys.argv[1])
    print [round(i*1000)/1000.0 for i in [price * 0.92, price * 0.96, price * 1.04, price * 1.08]]
