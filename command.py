# -*- coding: utf-8 -*-
import flags

class SyntaxE(flags.Flags):
    Slack = 1
    Ahead = 2
    Next = 4

class node:
    def __init__(self, conditions, owncommand, commandlist = [], decorator=lambda inp: inp, syntax=SyntaxE.Ahead):
        self.Conditions = conditions
        self.OwnCommand = owncommand
        self.Decorator = decorator
        self.CommandList = commandlist
        self.Syntax = syntax

