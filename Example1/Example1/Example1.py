import datetime
import time

three = [
    (["ahoj","cus"],
     lambda: print("nazdar")),
    (["se mas","ti je"],
     lambda: print("celkem fajn")),
    (["datum"],
     lambda: print(datetime.datetime.now().strftime("%Y/%m/%d"))),
    (["cas","hodin"],
     lambda: print(datetime.datetime.now().strftime("%H:%M:%S"))),
    ]

while True:
    inp = input()
    for tuple in three: 
        if any(condition in inp.lower() for condition in tuple[0]):
            tuple[1]()


# Zkus do konzole napsat neco jako: Ahoj, jak se mas?