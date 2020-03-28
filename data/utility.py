# -*- coding: utf-8 -*-
import unicodedata
import pygame
import gtts
import io


def TTS(strs):
    bytest = io.BytesIO()
    tts = gtts.gTTS(strs,lang="cs")
    tts.write_to_fp(bytest)
    isMixerInited = True
    bytest.seek(0)
    pygame.mixer.music.load(bytest)
    pygame.mixer.music.play()

def any_common(a, b): 
    a_set = set(a) 
    b_set = set(b) 
    if (a_set & b_set): 
        return True 
    else: 
        return False

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')