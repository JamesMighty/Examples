# -*- coding: utf-8 -*-
from flags import Flags

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
         useRegex=False, desiredEnd = ".",
         doOnlyOneFromSubthree = False):
        self.Conditions = conditions
        self.OwnCommand = owncommand
        self.Decorator = decorator
        self.CommandList = commandlist
        self.Syntax = syntax
        self.UseRegex = useRegex
        self.DesiredEnd = desiredEnd
        self.DoOnlyOneFromSubthree = doOnlyOneFromSubthree

class DoOnlyOne(Node):
    def __init__(self,
     commandlist,
     decorator=None,
     syntax=SyntaxE.Ahead,
     useRegex=False,
     desiredEnd='.',
     doOnlyOneFromSubthree=True):
        super().__init__(
            [""],
            None,
            commandlist=commandlist,
            decorator=decorator,
            syntax=syntax,
            useRegex=useRegex,
            desiredEnd=desiredEnd,
            doOnlyOneFromSubthree=doOnlyOneFromSubthree
        )

