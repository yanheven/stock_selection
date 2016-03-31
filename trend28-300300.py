from get_csv import read_csv

if __name__ == '__main__':
    # p1 = read_csv('399905.csv')
    p1 = read_csv('399008.csv')
    p2 = read_csv('399300.csv')
    lenght = len(p1)
    # lenght = 1445
    p2 = p2[:lenght]
    # p1 = p1[:lenght]
    p1 = p1[::-1]
    p2 = p2[::-1]
    p1.pop()
    p2.pop()
    lenght -= 1
    print(lenght)
    # lenght = 1444
    p11 = p1[:]
    p22 = p2[:]
    for i in xrange(lenght):
        p1[i] = float(p1[i][3])
        p2[i] = float(p2[i][3])
    balance = 10000
    fixed_pro = 0.027 / 365
    fee = 0.004 / 365
    hold_stock = ''
    hold_price = 0
    balance *= (1 + fixed_pro) ** 20
    internal = 20
    threadhold = 0.0
    for i in xrange(internal, lenght-1):
        if hold_stock:
            balance -= balance * fee
        else:
            balance += balance * fixed_pro
        p1_minus = p1[i] * 1.0 / p1[i-internal] - 1
        p2_minus = p2[i] * 1.0 / p2[i-internal] - 1
        if p1_minus > threadhold:
            if p1_minus > p2_minus:
                # buy p1
                if hold_stock != 'p1':
                    if hold_stock == 'p2':
                        balance *= (p2[i+1] * 1.0 / hold_price)
                    hold_price = p1[i+1]
                    hold_stock = 'p1'
            else:
                # buy p2
                if hold_stock != 'p2':
                    if hold_stock == 'p1':
                        balance *= (p1[i+1] * 1.0 / hold_price)
                    hold_price = p2[i+1]
                    hold_stock = 'p2'
        elif p2_minus > threadhold:
            # buy p2
            if hold_stock != 'p2':
                if hold_stock == 'p1':
                    balance *= (p1[i+1] * 1.0 / hold_price)
                hold_price = p2[i+1]
                hold_stock = 'p2'
        else:
            if hold_stock == 'p1':
                balance *= (p1[i+1] * 1.0 / hold_price)
            elif hold_stock == 'p2':
                balance *= (p2[i+1] * 1.0 / hold_price)
            hold_stock = ''
        print(p1[i], p2[i], balance)
    print(balance)