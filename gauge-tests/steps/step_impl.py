from getgauge.python import step, before_scenario, Messages
import resolver
import nodeThree
from command import *

@step("The node <node> has ahead syntax with argument node <arg>")
def node_has_ahead_syntax(node, arg):
    inp = node+" "+arg
    todo, inp2 = resolver.Resolve(nodeThree.Three, inp=inp,allResolvedMatches=[])
    print(todo)
    assert SyntaxE.Ahead in todo[0][1].Syntax, "node does not have SyntaxE.Ahead set"
    assert len(todo[0][2]) > 0, "node does not have any sub-todolist"
    outp = resolver.Do(todo,inp)
    return

@before_scenario()
def before_scenario_hook():
    return
