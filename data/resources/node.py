# -*- coding: utf-8 -*-
from data.lib.datastore.context import ContextRootProvider, ContextSubscriber
import data.lib.utility as util
from flags import Flags
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from data.api.resolver import Resolver


class SyntaxTypes(Flags):
    """
    does not matter where the condition is found in the query
    """
    Slack = 1
    """
    condition must be found before the conditions of subtree
    """
    Ahead = 2
    """
    condition must be found after the condition of subtree
    """
    Next = 4


class Node(ContextSubscriber):
    def __init__(self,
                 conditions,
                 own_command: Callable,
                 sub_tree=[],
                 decorator=None,
                 syntax: SyntaxTypes = SyntaxTypes.Ahead,
                 use_regex=False,
                 desired_end=".",
                 do_only_one_from_subtree=False,
                 do_remember_after_done=True,
                 do_negate_condition=False,
                 cleanup=None,
                 init=None
                 ):
        self.conditions = conditions
        self.own_command = own_command
        self.decorator = decorator
        self.subtree = sub_tree
        self.syntax = syntax
        self.use_regex = use_regex
        self.desired_end = desired_end
        self.do_only_one_from_subtree = do_only_one_from_subtree
        self.do_remember_when_done = do_remember_after_done
        self.do_negate_condition = do_negate_condition
        self._cleanup = cleanup
        self._initialization = init

        super().__init__()

    def initialization(self, resolver: 'Resolver', parentNode=None):
        self._contextPayload = {
            'syntax': str(self.syntax),
            'useRegex': self.use_regex,
            'conditions': self.conditions
        }
        if parentNode:
            self.subscribe(parentNode)
        else:
            self.subscribe(resolver)
        self.subscribedContext.update(self._contextPayload)
        if self._initialization:
            self._initialization(self, resolver)

    def clean_up(self, resolver: 'Resolver'):
        self.unsubscribe()
        if self._cleanup:
            self._cleanup(self, resolver)


class DoOnlyOne(Node):
    def __init__(self,
                 sub_tree,
                 decorator=None,
                 ):
        super().__init__(
            [""],
            None,
            sub_tree=sub_tree,
            decorator=decorator,
            syntax=SyntaxTypes.Slack,
            use_regex=False,
            desired_end="",
            do_only_one_from_subtree=True,
            do_remember_after_done=False,
            do_negate_condition=False,
            cleanup=None,
            init=None
        )


class Find(Node):
    def __init__(self,
                 conditions,
                 sub_tree,
                 decorator=None,
                 desired_end='.',
                 syntax=SyntaxTypes.Ahead,
                 use_regex=False,
                 do_negate_condition=False,
                 cleanUp=None,
                 init=None
                 ):
        super().__init__(
            conditions,
            None,
            sub_tree=sub_tree,
            decorator=decorator,
            syntax=syntax,
            use_regex=use_regex,
            desired_end=desired_end,
            do_only_one_from_subtree=False,
            do_remember_after_done=False,
            do_negate_condition=do_negate_condition,
            cleanup=cleanUp,
            init=init
        )


class RegexNode(Node):
    def __init__(self,
                 conditions,
                 own_command,
                 sub_tree=[],
                 decorator=None,
                 desired_end='.',
                 syntax=SyntaxTypes.Ahead,
                 do_negate_condition=False,
                 cleanUp=None,
                 init=None
                 ):
        super().__init__(
            conditions,
            own_command,
            sub_tree=sub_tree,
            decorator=decorator,
            syntax=syntax,
            use_regex=True,
            desired_end=desired_end,
            do_only_one_from_subtree=False,
            do_remember_after_done=False,
            do_negate_condition=do_negate_condition,
            cleanup=cleanUp,
            init=init
        )
