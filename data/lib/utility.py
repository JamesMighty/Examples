# -*- coding: utf-8 -*-
import unicodedata


def any_common(a, b):
    a_set = set(a)
    b_set = set(b)
    if (a_set & b_set):
        return True
    else:
        return False


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

    """
    flattens specified list
    """
def flatten(t):
    return [item for sublist in t for item in sublist]

