import datetime
import time
import unicodedata
import re

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

three = [
    (["ahoj","cus"],
     lambda inp: print("nazdar"),
     [
         (["se mas", "ti je"], lambda inp: print("celkem fajn"))
     ]
    ),
    (["se mas","ti je"],
     lambda inp: print("na prd")
    ),
    (["datum"],
     lambda inp: print(datetime.datetime.now().strftime("%Y/%m/%d"))
    ),
    (["cas","hodin"],
     lambda inp: print(datetime.datetime.now().strftime("%H:%M:%S"))
    ),
    (["chapes?","neopic"],
     lambda inp: print(inp)
    ),
    (["s{3}"],
     lambda inp: print("nope")
    )
    ]

def Resolve(three, inp=None):
    doPrintUnresolved = True
    resolved = False
    if inp == None:
        inp = strip_accents(input().lower())
    else:
        doPrintUnresolved = False
    for tuple in three: 
        if any((string in inp or re.match(string,inp)) for string in tuple[0]):
            tuple[1](inp)
            resolved = True
            if len(tuple) == 3:
                if Resolve(tuple[2],inp):    
                    break   
    if doPrintUnresolved and not resolved:
        print("co?")
    return resolved

while True:
    Resolve(three)


# Zkus do konzole napsat neco jako: Ahoj, jak se mas? nebo Ahoj, kolik je hodin?