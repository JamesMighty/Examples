# -*- coding: utf-8 -*-
from data.nodeThree import Three
import data.resolver as resolver
from data.utility import TTS
import pygame

pygame.mixer.init()
while True:
    inp = input("> ")
    todo = resolver.Resolve(Three, inp=inp, allResolvedMatches=[], lastMatch=0, doPrintUnresolved=True)[0]
    #print(todo)
    outp = resolver.Do(todo,inp)
    print(outp)
    TTS(outp)


# Zkus do konzole napsat neco jako: Ahoj, jak se mas? nebo Ahoj, kolik je hodin?