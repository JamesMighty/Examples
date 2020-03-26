# -*- coding: utf-8 -*-
from flags import Flags

class SyntaxE(Flags):
    Slack = 1
    Ahead = 2
    Next = 4

class Node:
    def __init__(self, conditions, owncommand, commandlist = [], decorator=lambda inp: inp, syntax=SyntaxE.Ahead, useRegex=False, desiredEnd = "."):
        self.Conditions = conditions
        self.OwnCommand = owncommand
        self.Decorator = decorator
        self.CommandList = commandlist
        self.Syntax = syntax
        self.UseRegex = useRegex
        self.DesiredEnd = desiredEnd

