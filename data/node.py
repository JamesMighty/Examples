# -*- coding: utf-8 -*-
from flags import Flags
import data.utility as util

class SyntaxE(Flags):
    Slack = 1
    Ahead = 2
    Next = 4

class Node:
    def __init__(self,
         conditions,
         owncommand,
         commandlist = [],
         decorator=None,
         syntax=SyntaxE.Ahead,
         useRegex=False,
         desiredEnd = ".",
         doOnlyOneFromSubthree = False,
         doRememberWhenDone = True
         ):
        self.Conditions = conditions
        self.OwnCommand = owncommand
        self.Decorator = decorator
        self.CommandList = commandlist
        self.Syntax = syntax
        self.UseRegex = useRegex
        self.DesiredEnd = desiredEnd
        self.DoOnlyOneFromSubthree = doOnlyOneFromSubthree
        self.DoRememberWhenDone = doRememberWhenDone

class DoOnlyOne(Node):
    def __init__(self,
     commandlist,
     decorator=None,
     desiredEnd='.',
     ):
        super().__init__(
            [""],
            None,
            commandlist=commandlist,
            decorator=decorator,
            syntax=SyntaxE.Slack,
            useRegex=False,
            desiredEnd=desiredEnd,
            doOnlyOneFromSubthree=True,
            doRememberWhenDone=False
        )

