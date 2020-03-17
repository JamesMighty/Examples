import enum

class SyntaxE(enum.Enum):
    First = 1
    Last = 2
    Slack = 4

class node:
    def __init__(self, conditions, owncommand, commandlist = [], decorator=lambda inp: inp, syntax=SyntaxE.First):
        self.Conditions = conditions
        self.OwnCommand = owncommand
        self.Decorator = decorator
        self.CommandList = commandlist
        self.Syntax = syntax

