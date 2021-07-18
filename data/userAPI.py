import data.resolver as resolver



def ChangeUsername(context, username = None):
    if username == None:
        context["username"] = input("Zadej své jméno: ")
        context["padding"] = len(context["username"]) + 3
    else:
        context["username"] = username
        context["padding"] = len(context["username"]) + 3
    return f"Uživatelské jméno změněno na {context['username']}"

def ChangeOutputFormat(context, format=None):
    if format == None:
        context["indexation"] = input("Zadej output format: ")
    else:
        context["indexation"] = format
    return f"Output format změněn na {context['indexation']}"

def TurnTTS(context, IsOn):
    context["DoSpeak"] = IsOn
    return "No dobrá" if IsOn else "Už mlčím"

def GetHelp(three, makeHeader=True, padding=3):
    if makeHeader:
        output = "Možné příkazy:\n"
    else:
        output = ""
    for node in three:
        output += f"{'':{padding}}-{node.Conditions}<{type(node).__name__}>\n"
        if len(node.SubThree)>0:
            output += GetHelp(node.SubThree, makeHeader=False, padding=padding+3)
    return output

def GetContextAnswerForSettings(context,var):
    if var == "DoSpeak":
        if context[var]:
            return "Vždyť mluvím"
        else:
            return "Můžu, ale nechci"
            
