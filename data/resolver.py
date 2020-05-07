# -*- coding: utf-8 -*-
from data.utility import *
from data.node import *
from data.todoItem import TodoItem
from data.match import Match
import data.nodeThree as nodeThree
import re
import json


class Resolver:

    def __init__(self, context = None, rootThree = None):
        if context != None:
            self.Context = context
        if rootThree != None:
            self.RootThree = rootThree

    def Do(self, todoList, inp):
        todoList = sorted(todoList, key = lambda item: item.MatchIndex)
        wholeOutput = ""
        for item in todoList:
            outp = None
            if item.Command.OwnCommand != None:
                if len(item.RegexGroups) > 0:
                    outp = item.Command.OwnCommand(self.Context, inp, item.RegexGroups)
                else:
                    outp = item.Command.OwnCommand(self.Context, inp)
            wholeOutput += (outp + (", " if len(item.SubTodoList) > 0 else item.Command.DesiredEnd + " ") if outp is not None else "" ) 
            if len(item.SubTodoList) > 0:
                wholeOutput += self.Do(item.SubTodoList,inp)
        return wholeOutput

    def SyntaxCheck(self, lastMatch, matchOn, syntaxSetting):
        isConditionFirst = lastMatch <= matchOn if SyntaxE.Ahead in syntaxSetting else True
        isConditionLast = lastMatch >= matchOn if SyntaxE.Next in syntaxSetting else True
        return isConditionFirst and isConditionLast

    def Resolve(self, three=None, inp=None, allResolvedMatches=[], lastMatch=0, doPrintUnresolved=False, syntaxSetting=SyntaxE.Ahead, doOnlyOne=False):
        if three == None:
            three = self.RootThree
        resolved = False
        todo = []
        if inp == None:
            inp = stripAccents(input(f"{self.Context['username']:{self.Context['padding']}}{self.Context['indexation']} ").lower())
        else:
            inp = stripAccents(inp.lower())
        for comm in three: 
            #print(f"checking: {comm.Conditions}")
            if comm.UseRegex:
                matches = [Match(re.search(string, inp).span()[0], string, re.findall(string, inp)) for string in comm.Conditions if re.search(string,inp) is not None]
            else:
                matches = [Match(inp.index(string),string) for string in comm.Conditions if string in inp]
            if len(matches) > 0:
                #print(matches)
                matchOn = min([match.Index for match in matches])
                if not anyCommon([match.String for match in matches],[resolvedMatch.String for resolvedMatch in allResolvedMatches]) and self.SyntaxCheck(lastMatch, matchOn, syntaxSetting):
                    #print(f"passed: {comm.Conditions}")
                    if comm.Decorator != None:
                        inp = comm.Decorator(inp)
                    resolved = True
                    if comm.DoRememberWhenDone:
                        allResolvedMatches+=matches
                    if len(comm.SubThree) > 0:
                        additionalTodo = self.Resolve(comm.SubThree,inp,allResolvedMatches, lastMatch=matchOn, doPrintUnresolved=False,syntaxSetting=comm.Syntax,doOnlyOne=comm.DoOnlyOneFromSubthree)[0]
                        todo.append( TodoItem(matchOn,comm, additionalTodo, [match.RegexGroups for match in matches if match.RegexGroups is not None]) )
                    else:
                        todo.append( TodoItem(matchOn,comm, [], [match.RegexGroups for match in matches if match.RegexGroups is not None]) )
                    if doOnlyOne:
                        break
                #else:
                    #print(f"skipped: {comm.Conditions}")
            #else:
                #print(f"no match: {comm.Conditions}")
        #print([match.__dict__ for match in allResolvedMatches])       
        if doPrintUnresolved and not resolved:
            todo.append(TodoItem(0,Node([],lambda inp: "co",desiredEnd="?"),[]))
        return todo,inp