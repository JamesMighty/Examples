# -*- coding: utf-8 -*-
from data.node import *
import datetime
import data.userAPI as uapi

global RootThree
RootThree = [
    Node(["ahoj","cus"],
     lambda setx, inp: "nazdar",
     [
         Node(["se mas", "ti je"], 
          lambda setx, inp: "mám se celkem fajn"
         )
     ]
    ),
    CheckFor(["pls"],
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
    Node(["pomoc","co?"],
     lambda setx, inp: print(RootThree)
    ),
    RegexNode(["co (.*) delas"],
     lambda setx, inp, kw: "idk, " + str(kw[0][0]),
     desiredEnd="?"
    ),
    CheckFor(["zmen", "uprav"],
     [
         DoOnlyOne([
            RegexNode(["format na '(.*)'"],
                lambda setx, inp, kw: uapi.ChangeOutputFormat(setx, format=kw[0][0]),
            ),
            Node(["format"],
                lambda setx, inp: uapi.ChangeOutputFormat(setx)
            )
         ]),
         DoOnlyOne([
            RegexNode(["jmeno na '(.*)'"],
                lambda setx, inp, kw: uapi.ChangeUsername(setx, username=kw[0][0]),
            ),
            Node(["jmeno"],
                lambda setx, inp: uapi.ChangeUsername(setx)
            )
         ])
     ])


    ]