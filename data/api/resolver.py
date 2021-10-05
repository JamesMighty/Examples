# -*- coding: utf-8 -*-
import json
import re
from typing import Any, ContextManager, List, Tuple

import data.model.nodeTree as nodeThree
import data.model.specialresponses as specialresponses
from data.lib.datastore.context import Context, ContextRootProvider
from data.lib.datastore.datastore import DatastoreRootProvider
from data.lib.utility import *
from data.resources.match import Match
from data.resources.node import *
from data.resources.todoItem import TodoItem


class Resolver(ContextRootProvider):

    def __init__(self, contextPayload = None, rootThree = None):
        if rootThree != None:
            self.RootThree = rootThree
        super().__init__(contextPayload)
    
    @ContextRootProvider.datastore.getter
    def globalContext(self) -> Context:
        return self.context
    
    def tts(self, strs):
        if strs != "" and self.globalContext["DoSpeak"]:
            bytest = io.BytesIO()
            tts = gtts.gTTS(strs,lang="cs")
            tts.write_to_fp(bytest)
            isMixerInited = True
            bytest.seek(0)
            pygame.mixer.music.load(bytest)
            pygame.mixer.music.play()

    def do(self, todoList:list[TodoItem], query:str, parentNode=None):
        # sort by regex math index from query input 
        todoList = sorted(todoList, key = lambda item: item.match_index)
        wholeOutput = ""
        for item in todoList:
            outp = None
            # initialize
            if item.node.initialization != None:
                item.node.initialization(self, parentNode)
            if item.node.own_command != None:
                try:
                    if len(item.regex_groups) > 0:
                        outp = item.node.own_command(self, query, item.regex_groups)
                    else:
                        outp = item.node.own_command(self, query)
                except Exception as e:
                    outp = str(e)
            lineEnd = (", " if len(item.subtodo_list) > 0 else item.node.desired_end + " ") if outp is not None else "" 
            wholeOutput += str(outp) + lineEnd
            if len(item.subtodo_list) > 0:
                wholeOutput += self.do(item.subtodo_list,query,parentNode=item.node)
            # teardown
            if item.node.clean_up != None:
                item.node.clean_up(self.globalContext)
        return wholeOutput
    
    def add_to_context(self, tuple: Tuple[str,Any]):
        self.globalContext[tuple[0]] = tuple[1]
    
    def add_to_history(self, tuple: Tuple[str,str]):
        self.globalContext["_history"][tuple[0]] = tuple[1]
        self.globalContext["_history"].save()

    def syntax_check(self, lastMatch, matchOn, syntaxSetting):
        isConditionFirst = lastMatch <= matchOn if SyntaxTypes.Ahead in syntaxSetting else True
        isConditionLast = lastMatch >= matchOn if SyntaxTypes.Next in syntaxSetting else True
        return isConditionFirst and isConditionLast

    def resolve(self, query):
        return self.resolve(self, query=query)

    def resolve(self, tree=None, query=None, allResolvedMatches=[], lastMatch=0, doPrintUnresolved=False, syntaxSetting=SyntaxTypes.Ahead, doOnlyOne=False):
        resolved = False
        todo = []

        if tree == None:
            tree = self.RootThree
        if query == None:
            consoleinput = input(f"{self.globalContext['username']:{self.globalContext['padding']}}{self.globalContext['indexation']} ")
            query = strip_accents(consoleinput.lower())
        else:
            query = strip_accents(query.lower())

        for node in tree: 
            #print(f"checking: {comm.Conditions}")
            if node.use_regex:
                matches = [Match(re.search(string, query).span()[0], string, re.findall(string, query)) for string in node.conditions if re.search(string,query) is not None]
            else:
                matches = [Match(query.index(string),string) for string in node.conditions if string in query]
            if len(matches) > 0 or (node.do_negate_condition and len(matches) == 0):
                #print(matches)
                matchOn = min([match.Index for match in matches])
                if (node.do_negate_condition and len(matches) == 0) or (not any_common([match.String for match in matches],[resolvedMatch.String for resolvedMatch in allResolvedMatches]) and self.syntax_check(lastMatch, matchOn, syntaxSetting)):
                    #print(f"passed: {comm.Conditions}")
                    
                    if node.do_remember_when_done:
                        allResolvedMatches+=matches

                    regexes = [match.RegexGroups for match in matches if match.RegexGroups is not None]
                    if len(node.subtree) > 0:
                        # node has children, resolve them too
                        if node.decorator != None:
                            subThreeInp = node.decorator(query)
                        else:
                            subThreeInp = query
                        additionalTodo = self.resolve(
                            node.subtree,
                            subThreeInp,
                            allResolvedMatches,
                            lastMatch=matchOn, 
                            doPrintUnresolved=False,
                            syntaxSetting=node.syntax,
                            doOnlyOne=node.do_only_one_from_subtree
                            )[0]
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


