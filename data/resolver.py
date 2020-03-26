# -*- coding: utf-8 -*-
from data.utility import *
from data.node import *
from data.todoItem import *
import re

def Do(todoList, inp):
    todoList = sorted(todoList, key = lambda item: item.MatchIndex)
    wholeOutput = ""
    for item in todoList:
        outp = None
        if len(item.RegexGroups) > 0:
            #print(item.RegexGroups)
            outp = item.Command.OwnCommand(inp, item.RegexGroups)
        else:
            outp = item.Command.OwnCommand(inp)
        wholeOutput += (outp + (", " if len(item.SubCommandThree) > 0 else ". ") if outp is not None else "" ) 
        if len(item.SubCommandThree) > 0:
            wholeOutput += Do(item.SubCommandThree,inp)
    return wholeOutput

def SyntaxCheck(lastMatch, matchOn, syntaxSetting):
    isConditionFirst = lastMatch <= matchOn if SyntaxE.Ahead in syntaxSetting else True
    isConditionLast = lastMatch >= matchOn if SyntaxE.Next in syntaxSetting else True
    return isConditionFirst and isConditionLast

def Resolve(three, inp=None, allResolvedMatches=[], lastMatch=0, doPrintUnresolved=False, syntaxSetting=SyntaxE.Ahead):
    resolved = False
    todo = []
    if inp == None:
        inp = strip_accents(input("> ").lower())
    else:
        inp = strip_accents(inp.lower())
    for comm in three: 
        matches = [(inp.index(string),string, None) for string in comm.Conditions if string in inp] + [(re.search(string, inp).span()[0], string, re.findall(string, inp)) for string in comm.Conditions if re.search(string,inp) is not None and comm.UseRegex]
        if len(matches) > 0:
            #print(matches)
            matchOn = min([match[0] for match in matches])
            if not any_common([match[1] for match in matches],[resolvedMatch[1] for resolvedMatch in allResolvedMatches]) and SyntaxCheck(lastMatch, matchOn, syntaxSetting):
                inp = comm.Decorator(inp) # not used
                resolved = True
                allResolvedMatches+=matches
                if len(comm.CommandList) > 0:
                    additionalTodo = Resolve(comm.CommandList,inp,allResolvedMatches, lastMatch=matchOn, doPrintUnresolved=False,syntaxSetting=comm.Syntax)[0]
                    todo.append( todoItem(matchOn,comm, additionalTodo, [match[2] for match in matches if match[2] is not None]) )
                else:
                    todo.append( todoItem(matchOn,comm, [], [match[2] for match in matches if match[2] is not None]) )
            
    if doPrintUnresolved and not resolved:
        print("co?")
    return todo,inp