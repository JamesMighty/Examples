from utility import *
import re

def Do(todoList, inp):
    todoList = sorted(todoList, key = lambda item: item[0])
    wholeOutput = "" # sberac
    for item in todoList:
        outp = item[1].OwnCommand(inp) # vlastni vystup
        wholeOutput += (outp if outp is not None else "" ) + " "
        if len(item[2]) > 0:
            wholeOutput += Do(item[2],inp)
    return wholeOutput

def Resolve(three, inp=None, allResolvedStrings=[]):
    doPrintUnresolved = True
    resolved = False
    todo = []
    if inp == None:
        inp = strip_accents(input("> ").lower())
    else:
        inp = strip_accents(inp.lower())
        doPrintUnresolved = False
    for comm in three: 
        matchingStrings = [string for string in comm.Conditions if string in inp] + [string for string in comm.Conditions if re.search(string,inp) is not None]
        indexes = [inp.index(string) for string in comm.Conditions if string in inp ] + [re.search(string, inp).span()[0] for string in comm.Conditions  if re.search(string,inp) is not None]
        if len(matchingStrings) > 0 and not any_common(matchingStrings,allResolvedStrings):
            inp = comm.Decorator(inp) # mozna se bude nekdy hodit, idk
            resolved = True
            allResolvedStrings+=matchingStrings
            if len(comm.CommandList) > 0:
                todo.append( (min(indexes),comm, Resolve(comm.CommandList,inp,allResolvedStrings)[0]) )
            else:
                todo.append( (min(indexes),comm, []) )
            
    if doPrintUnresolved and not resolved:
        print("co?")
    #print(allResolvedStrings)
    return todo,inp