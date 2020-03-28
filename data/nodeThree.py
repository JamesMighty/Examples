# -*- coding: utf-8 -*-
from data.node import *
import datetime

global Three
Three = [
    Node(["ahoj","cus"],
     lambda inp: "nazdar",
     [
         Node(["se mas", "ti je"], 
          lambda inp: "mám se celkem fajn"
         )
     ]
    ),
    Node(["pls"],
     lambda inp: None,
     [
         Node(["se mas"],
          lambda inp: "naprosto skvěle"
         )
     ],
     syntax=SyntaxE.Slack
    ),
    Node(["se mas","ti je"],
     lambda inp: "na prd"
    ),
    Node(["datum"],
     lambda inp: datetime.datetime.now().strftime("%Y/%m/%d")
    ),
    Node(["cas","hodin", "kolik je"],
     lambda inp: "právě je "+datetime.datetime.now().strftime("%H:%M:%S")
    ),
    Node(["neopic"],
     lambda inp: inp,
     [
         Node(["prosim"],
            lambda inp: "ok sry"
         )
     ]
    ),
    Node(["s{3}"],
     lambda inp: "nope",
     useRegex=True
    ),
    Node(["pomoc","co?"],
     lambda inp: print(Three)
    ),
    Node(["co (.*) delas"],
     lambda inp, kw: "idk, " + str(kw[0][0]),
     useRegex=True,
     desiredEnd="?"
    )
    ]