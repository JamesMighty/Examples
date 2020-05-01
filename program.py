# -*- coding: utf-8 -*-
from data.nodeThree import Three
import data.resolver as resolver
from data.utility import TTS
import pygame

pygame.mixer.init()

name = input("Zadej své jméno: ") # Pak to vysperkujeme na users nebo tak slo mi jen o vzhled

while True:
    inp = input(name + "-> ") # co se tice toho znaku -> nic lepsiho me nenapadlo ale mužes si vybrat  May:>, May>>>, May:, atd. 
    todo = resolver.Resolve     (Three, inp=inp, allResolvedMatches=[], lastMatch=0, doPrintUnresolved=True)[0]
    #print(todo)
    outp = resolver.Do(todo,inp)
    print("May-> " + outp)
    TTS(outp)


# Zkus do konzole napsat neco jako: Ahoj, jak se mas? nebo Ahoj, kolik je hodin?
