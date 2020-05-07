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
         subThree = [],
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
        self.SubThree = subThree
        self.Syntax = syntax
        self.UseRegex = useRegex
        self.DesiredEnd = desiredEnd
        self.DoOnlyOneFromSubthree = doOnlyOneFromSubthree
        self.DoRememberWhenDone = doRememberWhenDone

class DoOnlyOne(Node):
    def __init__(self,
     subThree,
     decorator=None,
     desiredEnd='.',
     ):
        super().__init__(
            [""],
            None,
            subThree=subThree,
            decorator=decorator,
            syntax=SyntaxE.Slack,
            useRegex=False,
            desiredEnd=desiredEnd,
            doOnlyOneFromSubthree=True,
            doRememberWhenDone=False
        )

class CheckFor(Node):
    def __init__(self,
     conditions,
     subThree,
     decorator=None,
     desiredEnd='.',
     syntax=SyntaxE.Ahead,
     useRegex=False
     ):
        super().__init__(
            conditions,
            None,
            subThree=subThree,
            decorator=decorator,
            syntax=syntax,
            useRegex=useRegex,
            desiredEnd=desiredEnd,
            doOnlyOneFromSubthree=False,
            doRememberWhenDone=False
        )

class RegexNode(Node):
    def __init__(self,
     conditions,
     owncommand,
     subThree=[],
     decorator=None,
     desiredEnd='.',
     syntax=SyntaxE.Ahead,
     ):
        super().__init__(
            conditions,
            owncommand,
            subThree=subThree,
            decorator=decorator,
            syntax=syntax,
            useRegex=True,
            desiredEnd=desiredEnd,
            doOnlyOneFromSubthree=False,
            doRememberWhenDone=False
        )