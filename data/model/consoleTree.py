# -*- coding: utf-8 -*-
import datetime

import data.api.consoletreeapi as cmdapi
import data.api.userAPI as uapi
from data.resources.node import *

ROOT_TREE = [
    Find(["run"], [
        RegexNode(["console \"(.*)\"","cmd \"(.*)\""],
            cmdapi.RunCmdCommand()
        )

    ]),
    Find(["show", "print"],[
        DoOnlyOne([
            Node(["context", "know"],
                uapi.GetContextCommand()
            ),
            Node(["history"],
                uapi.GetHistoryContextCommand()
            )
        ])
    ]),
    RegexNode(["run (.*)","start (.*)"],
        cmdapi.PopenCommand()
    )
]
