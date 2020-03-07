import datetime
import time
import unicodedata
import re

def any_common(a, b): 
    a_set = set(a) 
    b_set = set(b) 
    if (a_set & b_set): 
        return True 
    else: 
        return False

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

three = [
    (["ahoj","cus"],
     lambda inp: print("nazdar"),
     [
         (["se mas", "ti je"],
          lambda inp: print("celkem fajn")
         )
     ]
    ),
    (["se mas","ti je"],
     lambda inp: print("na prd")
    ),
    (["datum"],
     lambda inp: print(datetime.datetime.now().strftime("%Y/%m/%d"))
    ),
    (["cas","hodin", "kolik je"],
     lambda inp: print(datetime.datetime.now().strftime("%H:%M:%S"))
    ),
    (["neopic"],
     lambda inp: print(inp),
     [
         (["prosim"],
            lambda inp: [print("ok, sorry"),inp][-0]
         )
     ]
    ),
    (["s{3}"],
     lambda inp: print("nope")
    )
    ]

def Resolve(three, inp=None, allResolvedStrings=[]):
    doPrintUnresolved = True
    resolved = False
    if inp == None:
        inp = strip_accents(input("> ").lower())
    else:
        doPrintUnresolved = False
    for tuple in three: 
        matchingStrings = [string for string in tuple[0] if (string in inp or re.match(string,inp))]
        if len(matchingStrings) > 0 and not any_common(matchingStrings,allResolvedStrings):
            result = tuple[1](inp)
            resolved = True
            allResolvedStrings+=matchingStrings
            if len(tuple) == 3:
                Resolve(tuple[2],inp,allResolvedStrings)
    if doPrintUnresolved and not resolved:
        print("co?")
    #print(allResolvedStrings)
    return resolved

while True:
    Resolve(three, None, [])


# Zkus do konzole napsat neco jako: Ahoj, jak se mas? nebo Ahoj, kolik je hodin?