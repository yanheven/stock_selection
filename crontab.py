from time import sleep
from lowest import today_transaction


if __name__ == '__main__':
    while True:
        today_transaction()
        sleep(1800)
