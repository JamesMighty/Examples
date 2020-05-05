# -*- coding: utf-8 -*-
from data.node import *
import datetime
import data.userAPI as uapi

global Three
Three = [
    Node(["ahoj","cus"],
     lambda setx, inp: "nazdar",
     [
         Node(["se mas", "ti je"], 
          lambda setx, inp: "mám se celkem fajn"
         )
     ]
    ),
    Node(["pls"],
     lambda setx, inp: None,
     [
         Node(["se mas"],
          lambda setx, inp: "naprosto skvěle"
         )
     ],
     syntax=SyntaxE.Slack
    ),
    Node(["se mas","ti je"],
     lambda setx, inp: "na prd"
    ),
    Node(["datum"],
     lambda setx, inp: datetime.datetime.now().strftime("%Y/%m/%d")
    ),
    Node(["cas","hodin", "kolik je"],
     lambda setx, inp: "právě je "+datetime.datetime.now().strftime("%H:%M:%S")
    ),
    Node(["neopic"],
     lambda setx, inp: inp,
     [
         Node(["prosim"],
            lambda setx, inp: "ok sry"
         )
     ]
    ),
    Node(["s{3}"],
     lambda setx, inp: "nope",
     useRegex=True
    ),
    Node(["pomoc","co?"],
     lambda setx, inp: print(Three)
    ),
    Node(["co (.*) delas"],
     lambda setx, inp, kw: "idk, " + str(kw[0][0]),
     useRegex=True,
     desiredEnd="?"
    ),
    Node(["zmen"],
     None,
     [
         DoOnlyOne([
            Node(["jmeno na '(.*)'"],
                lambda setx, inp, kw: uapi.ChangeUsername(setx, username=kw[0][0]),
                useRegex=True
            ),
            Node(["jmeno"],
                lambda setx, inp: uapi.ChangeUsername(setx)
            )
         ]),
         Node(["format"],
            lambda setx, inp: uapi.ChangeOutputFormat(setx)
         )
     ]
    )
    ]