

class node:
    Conditions = []
    OwnCommand = lambda inp: inp
    CommandList = []
    Decorator = lambda inp: inp

    def __init__(self, conditions, owncommand, commandlist = [], decorator=lambda inp: inp):
        self.Conditions = conditions
        self.OwnCommand = owncommand
        self.Decorator = decorator
        self.CommandList = commandlist