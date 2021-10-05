

from typing import Callable,TYPE_CHECKING
if TYPE_CHECKING:
    from data.resources.node import Node


class TodoItem:
    def __init__(self, matchIndex:int, node:'Node', subCommandThree:list['Node'], regexGroups=[]):
        self.match_index = matchIndex
        self.node = node
        self.subtodo_list = subCommandThree
        self.regex_groups = regexGroups
