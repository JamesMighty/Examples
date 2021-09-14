# -*- coding: utf-8 -*-
import data.api.userAPI as uapi
import datetime

import data.api.consoletreeapi as cmdapi
from data.resources.node import *


ROOT_TREE = [
    Find(["run"], [
        RegexNode(["console \"(.*)\"","cmd \"(.*)\""],
            cmdapi.RunCmdCommand()
        )

    ]),
    Find(["show", "print"],[
        Node(["context", "know"],
            uapi.GetContextCommand()
        ),
        Node(["history"],
            uapi.GetHistoryContextCommand()
        )
    ]),
    RegexNode(["run (.*)"],
        cmdapi.PopenCommand()
    )
]
