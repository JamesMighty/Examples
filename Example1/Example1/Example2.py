import datetime
import time
import unicodedata

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

three = [
    (["ahoj","cus"],
     lambda: print("nazdar"),
     [
         (["se mas", "ti je"], lambda: print("celkem fajn"))
         ]),
    (["se mas","ti je"],
     lambda: print("na prd")),
    (["datum"],
     lambda: print(datetime.datetime.now().strftime("%Y/%m/%d"))),
    (["cas","hodin"],
     lambda: print(datetime.datetime.now().strftime("%H:%M:%S"))),
    ]

def Resolve(three, inp=None):
    doPrintUnresolved = True
    resolved = False
    if inp == None:
        inp = input()
    else:
        doPrintUnresolved = False
    for tuple in three: 
        if any(condition in strip_accents(inp.lower()) for condition in tuple[0]):
            tuple[1]()
            resolved = True
            if len(tuple) == 3:
                if Resolve(tuple[2],inp):    
                    break   
    if doPrintUnresolved and not resolved:
        print("co?")
    return resolved

while True:
    Resolve(three)


# Zkus do konzole napsat neco jako: Ahoj, jak se mas?