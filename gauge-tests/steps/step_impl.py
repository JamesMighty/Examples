from getgauge.python import step, before_scenario, Messages, DataStore
from data.api import resolver
from data.model import nodeThree
from data.resources.node import *


@step("The node <node> has syntax <flagName> with argument node <arg>")
def node_has_specified_syntax_flag(node,flagName, arg):
    flag = SyntaxTypes.from_str(flagName)
    print("Checking "+flagName+" syntax for "+node)

    print("     Ahead syntax check")
    inp = node+" "+arg
    todo, inp2 = resolver.Resolve(nodeThree.Three, inp=inp,allResolvedMatches=[])
    print(todo)
    if SyntaxTypes.Ahead in flag or SyntaxTypes.Slack in flag:
        assert len(todo[0].SubTodoList) > 0, "node does not have any sub-todolist when node before args"
    if SyntaxTypes.Next in flag:
        assert len(todo[0].SubTodoList) == 0, "node does have sub-todolist when node is after args"

    print("     Next syntax check")
    inp = arg+" "+node
    todo, inp2 = resolver.Resolve(nodeThree.Three, inp=inp,allResolvedMatches=[])
    print(todo)
    if SyntaxTypes.Next in flag or SyntaxTypes.Slack in flag:
        assert len(todo[0].SubTodoList) > 0, "node does not have sub-todolist when node is after args"
    if SyntaxTypes.Ahead in flag:
        assert len(todo[0].SubTodoList) == 0, "node does have sub-todolist when node is after args"

@before_scenario()
def before_scenario_hook():
    return
