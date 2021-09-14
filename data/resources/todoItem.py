

class TodoItem:
    def __init__(self, matchIndex, command, subCommandThree, regexGroups=[]):
        self.MatchIndex = matchIndex
        self.Command = command
        self.SubTodoList = subCommandThree
        self.RegexGroups = regexGroups