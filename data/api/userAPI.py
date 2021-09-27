import json
import data.api.resolver as resolver
from data.lib.datastore.context import Context
from data.resources.command import Command
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from data.api.resolver import Resolver


class GetContextCommand(Command):

    def __call__(self, resolver: 'Resolver', query: str, **kwargs) -> str:
        return resolver.globalContext

class GetHistoryContextCommand(Command):

    def __call__(self, resolver: 'Resolver', query: str, **kwargs) -> str:
        return str(resolver.globalContext["_history"])
        
def change_username(context, username = None):
    if username == None:
        context["username"] = input("Zadej své jméno: ")
        context["padding"] = len(context["username"]) + 3
    else:
        context["username"] = username
        context["padding"] = len(context["username"]) + 3
    return f"Uživatelské jméno změněno na {context['username']}"

def change_output_format(context, format=None):
    if format == None:
        context["indexation"] = input("Zadej output format: ")
    else:
        context["indexation"] = format
    return f"Output format změněn na {context['indexation']}"

def switch_tts(context, IsOn):
    context["DoSpeak"] = IsOn
    return "No dobrá" if IsOn else "Už mlčím"

def get_help(three, makeHeader=True, padding=3):
    if makeHeader:
        output = "Možné příkazy:\n"
    else:
        output = ""
    for node in three:
        output += f"{'':{padding}}-{node.Conditions}<{type(node).__name__}>\n"
        if len(node.SubThree)>0:
            output += get_help(node.SubThree, makeHeader=False, padding=padding+3)
    return output

def get_context_answer_for_settings(context,var):
    if var == "DoSpeak":
        if context[var]:
            return "Vždyť mluvím"
        else:
            return "Můžu, ale nechci"
            
