from datetime import datetime, timedelta
import time

first = datetime.now()
time.sleep(5)
second = datetime.now()

if second >= first+timedelta(minutes=4):
    print(second)

