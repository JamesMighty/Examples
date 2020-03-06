import datetime
import time

three = [
    (["ahoj","cus"],lambda: print("nazdar")),
    (["hodin"], lambda: print(str(datetime.date.today())))
    ]

while True:
    inp = input()
    for tuple in three:
        if any(condition in inp for condition in tuple[0]):
            tuple[1]()
