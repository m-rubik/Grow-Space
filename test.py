# from datetime import datetime, timedelta
# import time

# first = datetime.now()
# time.sleep(5)
# second = datetime.now()

# if second >= first+timedelta(minutes=4):
#     print(second)

from abc import ABC, abstractmethod

class Base(ABC):
    def __init__(self):
        print("Init")

    @abstractmethod
    def test(self):
        pass

class DerivedClass(Base):
    def __init__(self):
        super().__init__()

    def test(self):
        print("YEAH")

a = DerivedClass()
a.test()