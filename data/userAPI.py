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