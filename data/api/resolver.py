# -*- coding: utf-8 -*-
from data.lib.datastore.datastore import DatastoreProvider
import json
import re
from typing import Any, Tuple

import data.model.nodeTree as nodeThree
import data.model.specialresponses as specialresponses
from data.lib.utility import *
from data.lib.datastore.context import Context, ContextProvider
from data.resources.match import Match
from data.resources.node import *
from data.resources.todoItem import TodoItem


class Resolver(ContextProvider):

    def __init__(self, context = None, rootThree = None):
        if rootThree != None:
            self.RootThree = rootThree
        super().__init__(context)
    
    def tts(self, strs):
        if strs != "" and self.context["DoSpeak"]:
            bytest = io.BytesIO()
            tts = gtts.gTTS(strs,lang="cs")
            tts.write_to_fp(bytest)
            isMixerInited = True
            bytest.seek(0)
            pygame.mixer.music.load(bytest)
            pygame.mixer.music.play()

    def do(self, todoList, query):
        # sort by regex math index from query input 
        todoList = sorted(todoList, key = lambda item: item.MatchIndex)
        wholeOutput = ""
        for item in todoList:
            outp = None
            # initialize
            if item.Command.Initialization != None:
                item.Command.Initialization(self.context)
            if item.Command.OwnCommand != None:
                if len(item.RegexGroups) > 0:
                    outp = item.Command.OwnCommand(self.context, query, item.RegexGroups)
                else:
                    outp = item.Command.OwnCommand(self.context, query)
            lineEnd = (", " if len(item.SubTodoList) > 0 else item.Command.DesiredEnd + " ") if outp is not None else "" 
            wholeOutput += str(outp) + lineEnd
            if len(item.SubTodoList) > 0:
                wholeOutput += self.do(item.SubTodoList,query)
            if item.Command.CleanUp != None:
                item.Command.CleanUp(self.context)
        return wholeOutput
    
    def add_to_context(self, tuple: Tuple[str,Any]):
        self.context[tuple[0]] = tuple[1]
    
    def add_to_history(self, tuple: Tuple[str,str]):
        self.context["_history"][tuple[0]] = tuple[1]
        self.context["_history"].save()

    def syntax_check(self, lastMatch, matchOn, syntaxSetting):
        isConditionFirst = lastMatch <= matchOn if SyntaxE.Ahead in syntaxSetting else True
        isConditionLast = lastMatch >= matchOn if SyntaxE.Next in syntaxSetting else True
        return isConditionFirst and isConditionLast

    def resolve(self, query):
        return self.resolve(self, query=query)

    def resolve(self, tree=None, query=None, allResolvedMatches=[], lastMatch=0, doPrintUnresolved=False, syntaxSetting=SyntaxE.Ahead, doOnlyOne=False):
        resolved = False
        todo = []

        if tree == None:
            tree = self.RootThree
        if query == None:
            consoleinput = input(f"{self.context['username']:{self.context['padding']}}{self.context['indexation']} ")
            query = strip_accents(consoleinput.lower())
        else:
            query = strip_accents(query.lower())

        for node in tree: 
            #print(f"checking: {comm.Conditions}")
            if node.UseRegex:
                matches = [Match(re.search(string, query).span()[0], string, re.findall(string, query)) for string in node.Conditions if re.search(string,query) is not None]
            else:
                matches = [Match(query.index(string),string) for string in node.Conditions if string in query]
            if len(matches) > 0 or (node.DoNegateCondition and len(matches) == 0):
                #print(matches)
                matchOn = min([match.Index for match in matches])
                if (node.DoNegateCondition and len(matches) == 0) or (not any_common([match.String for match in matches],[resolvedMatch.String for resolvedMatch in allResolvedMatches]) and self.syntax_check(lastMatch, matchOn, syntaxSetting)):
                    #print(f"passed: {comm.Conditions}")
                    
                    if node.DoRememberWhenDone:
                        allResolvedMatches+=matches

                    regexes = [match.RegexGroups for match in matches if match.RegexGroups is not None]
                    if len(node.SubThree) > 0:
                        # node has children, resolve them too
                        if node.Decorator != None:
                            subThreeInp = node.Decorator(query)
                        else:
                            subThreeInp = query
                        additionalTodo = self.resolve(node.SubThree,subThreeInp,allResolvedMatches, lastMatch=matchOn, doPrintUnresolved=False,syntaxSetting=node.Syntax,doOnlyOne=node.DoOnlyOneFromSubthree)[0]
                        # add as todoItem with child todo list
                        item = TodoItem(matchOn,node, additionalTodo, regexes)
                        todo.append(item)
                    else:
                        # node has no children, proceed
                        item = TodoItem(matchOn,node, [], regexes)
                        todo.append(item)
                    resolved = True
                    if doOnlyOne:
                        break
                #else:
                    #print(f"skipped: {comm.Conditions}")
            #else:
                #print(f"no match: {comm.Conditions}")
        #print([match.__dict__ for match in allResolvedMatches])       
        if doPrintUnresolved and not resolved:
            todo.append(specialresponses.UNABLE_TO_RESOLVE)
        return todo,query


