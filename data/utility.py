# -*- coding: utf-8 -*-
import unicodedata
import pygame
import gtts
import io




def anyCommon(a, b): 
    a_set = set(a) 
    b_set = set(b) 
    if (a_set & b_set): 
        return True 
    else: 
        return False

def stripAccents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def ReportDecorator(inp, message=""):
    print(f"Got inp '{inp}'; message: {message}")
    return inp