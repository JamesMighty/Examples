import flags

class SyntaxE(flags.Flags):
    First = 1
    Last = 2
    Slack = 1 | 2

class node:
    def __init__(self, conditions, owncommand, commandlist = [], decorator=lambda inp: inp, syntax=SyntaxE.First):
        self.Conditions = conditions
        self.OwnCommand = owncommand
        self.Decorator = decorator
        self.CommandList = commandlist
        self.Syntax = syntax

