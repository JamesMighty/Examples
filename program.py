# -*- coding: utf-8 -*-
import json
import pygame
from data.api.resolver import Resolver
import data.api.userAPI as uapi
import data.model.generic as generic
from data.lib.datastore.context import Context
from data.model.consoleTree import ROOT_TREE

pygame.mixer.init()

context = generic.DEFAULT_CONTEXT
MayResolver = Resolver(contextPayload=context,rootThree=ROOT_TREE)
uapi.change_username(MayResolver.globalContext)

while True:
    inp = input(f"{MayResolver.globalContext['username']:{MayResolver.globalContext['padding']}}{MayResolver.globalContext['indexation']} ")
    todo = MayResolver.resolve(ROOT_TREE, query=inp, allResolvedMatches=[], lastMatch=0, doPrintUnresolved=True)[0]
    outp = MayResolver.do(todo,inp)
    MayResolver.add_to_history((inp,outp))
    print(f"{MayResolver.globalContext['AIName']:{MayResolver.globalContext['padding']}}{MayResolver.globalContext['indexation']} " + outp)
    MayResolver.tts(outp)
