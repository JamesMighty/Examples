# -*- coding: utf-8 -*-
from data.model.consoleTree import ROOT_TREE
import data.api.resolver as resolver
import data.api.userAPI as uapi
import data.model.generic as generic
from data.lib.datastore.context import Context
import pygame
import json

pygame.mixer.init()

context = generic.DEFAULT_CONTEXT
MayResolver = resolver.Resolver(context=context,rootThree=ROOT_TREE)
uapi.change_username(MayResolver.context)

while True:
    inp = input(f"{MayResolver.context['username']:{MayResolver.context['padding']}}{MayResolver.context['indexation']} ")
    todo = MayResolver.resolve(ROOT_TREE, query=inp, allResolvedMatches=[], lastMatch=0, doPrintUnresolved=True)[0]
    outp = MayResolver.do(todo,inp)
    MayResolver.add_to_history((inp,outp))
    print(f"{MayResolver.context['AIName']:{MayResolver.context['padding']}}{MayResolver.context['indexation']} " + outp)
    MayResolver.tts(outp)
