

class node:
    Conditions = []
    OwnCommand = lambda inp: inp
    CommandList = []
    Decorator = lambda inp: inp
    SlackSyntax = False

    def __init__(self, conditions, owncommand, commandlist = [], decorator=lambda inp: inp, slacksyntax=False):
        self.Conditions = conditions
        self.OwnCommand = owncommand
        self.Decorator = decorator
        self.CommandList = commandlist
        self.SlackSyntax = slacksyntax