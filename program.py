import datetime
import time
import unicodedata
import re
from command import node
from utility import *
from nodeThree import Three


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

    if len(todo) > 0 and doCommit:
        todo = sorted(todo, key = lambda tuple: tuple[0])
        for comm in todo:
            comm[1].OwnCommand(inp)
            
    if doPrintUnresolved and not resolved:
        print("co?")
    #print(allResolvedStrings)
    return todo

while True:
    Resolve(Three, None, [])


# Zkus do konzole napsat neco jako: Ahoj, jak se mas? nebo Ahoj, kolik je hodin?