from utility import *
import re

def Do(todoList, inp):
    todoList = sorted(todoList, key = lambda item: item[0])
    wholeOutput = ""
    for item in todoList:
        outp = item[1].OwnCommand(inp)
        wholeOutput += (outp + (", " if len(item[2]) > 0 else ". ") if outp is not None else "" ) 
        if len(item[2]) > 0:
            wholeOutput += Do(item[2],inp)
    return wholeOutput

def Resolve(three, inp=None, allResolvedMatches=[], lastMatch=0, doPrintUnresolved=False):
    resolved = False
    todo = []
    if inp == None:
        inp = strip_accents(input("> ").lower())
    else:
        inp = strip_accents(inp.lower())
    for comm in three: 
        matches = [(inp.index(string),string) for string in comm.Conditions if string in inp] + [(re.search(string, inp).span()[0], string) for string in comm.Conditions if re.search(string,inp) is not None]
        if len(matches) > 0:
            matchOn = min([match[0] for match in matches])
            if not any_common([match[1] for match in matches],[resolvedMatch[1] for resolvedMatch in allResolvedMatches]) and lastMatch <= matchOn:
                inp = comm.Decorator(inp) # mozna se bude nekdy hodit, idk
                resolved = True
                allResolvedMatches+=matches
                if len(comm.CommandList) > 0:
                    additionalTodo =  Resolve(comm.CommandList,inp,allResolvedMatches, lastMatch=matchOn, doPrintUnresolved=False)[0]
                    todo.append( (matchOn,comm, additionalTodo) )
                else:
                    todo.append( (matchOn,comm, []) )
            
    if doPrintUnresolved and not resolved:
        print("co?")
    return todo,inp