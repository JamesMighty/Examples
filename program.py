# -*- coding: utf-8 -*-
from data.nodeThree import RootThree
import data.resolver as resolver
from data.utility import TTS
import data.userAPI as uapi
import data.nodeThree as nodeThree
import pygame
import json

pygame.mixer.init()

context = {
    "AIName": "May",
    "indexation":"->",
    "username": None,
    "padding": 0
}

MayResolver = resolver.Resolver(context=context,rootThree=nodeThree.RootThree)
uapi.ChangeUsername(MayResolver.Context)

while True:
    inp = input(f"{MayResolver.Context['username']:{MayResolver.Context['padding']}}{MayResolver.Context['indexation']} ") # co se tice toho znaku -> nic lepsiho me nenapadlo ale mužes si vybrat  May:>, May>>>, May:, atd. 
    todo = MayResolver.Resolve(RootThree, inp=inp, allResolvedMatches=[], lastMatch=0, doPrintUnresolved=True)[0]
    outp = MayResolver.Do(todo,inp)
    print(f"{MayResolver.Context['AIName']:{MayResolver.Context['padding']}}{MayResolver.Context['indexation']} " + outp)
    TTS(outp)

# Zkus do konzole napsat neco jako: Ahoj, jak se mas? nebo Ahoj, kolik je hodin?
