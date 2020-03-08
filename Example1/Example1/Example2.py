import datetime
import time
import unicodedata
import re
from command import node

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
    node(["ahoj","cus"],
     lambda inp: print("nazdar"),
     [
         node(["se mas", "ti je"],
          lambda inp: print("mam se celkem fajn")
         )
     ]
    ),
    node(["se mas","ti je"],
     lambda inp: print("na prd")
    ),
    node(["datum"],
     lambda inp: print(datetime.datetime.now().strftime("%Y/%m/%d"))
    ),
    node(["cas","hodin", "kolik je"],
     lambda inp: print("prave je "+datetime.datetime.now().strftime("%H:%M:%S"))
    ),
    node(["neopic"],
     lambda inp: print(inp),
     [
         node(["prosim"],
            lambda inp: [print("ok, sorry"),inp][-0]
         )
     ]
    ),
    node(["s{3}"],
     lambda inp: print("nope")
    ),
    node(["pomoc","co?"],
     lambda inp: print( "\n".join([str(tupl[0]) for tupl in three]))
    )
    ]

def Resolve(three, inp=None, allResolvedStrings=[], doCommit=True):
    doPrintUnresolved = True
    resolved = False
    todo = []
    if inp == None:
        inp = strip_accents(input("> ").lower())
    else:
        doPrintUnresolved = False
    for comm in three: 
        matchingStrings = [string for string in comm.Conditions if (string in inp or re.match(string,inp))]
        indexes = [inp.index(string) for string in comm.Conditions if (string in inp or re.match(string,inp))]
        if len(matchingStrings) > 0 and not any_common(matchingStrings,allResolvedStrings):
            inp = comm.Decorator(inp) # mozna se bude nekdy hodit, idk
            todo.append( (min(indexes),comm) )
            resolved = True
            allResolvedStrings+=matchingStrings
            if len(comm.CommandList) > 0:
                todo += Resolve(comm.CommandList,inp,allResolvedStrings, doCommit=False) 

    if len(todo) is not 0 and doCommit:
        todo = sorted(todo, key = lambda tuple: tuple[0])
        for comm in todo:
            comm[1].OwnCommand(inp)
            
    if doPrintUnresolved and not resolved:
        print("co?")
    #print(allResolvedStrings)
    return todo

while True:
    Resolve(three, None, [])


# Zkus do konzole napsat neco jako: Ahoj, jak se mas? nebo Ahoj, kolik je hodin?