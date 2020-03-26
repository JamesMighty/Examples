# -*- coding: utf-8 -*-
from data.node import *
import datetime

global Three
Three = [
    node(["ahoj","cus"],
     lambda inp: "nazdar",
     [
         node(["se mas", "ti je"], 
          lambda inp: "mám se celkem fajn"
         )
     ]
    ),
    node(["pls"],
     lambda inp: None,
     [
         node(["se mas"],
          lambda inp: "naprosto skvěle"
         )
     ],
     syntax=SyntaxE.Slack
    ),
    node(["se mas","ti je"],
     lambda inp: "na prd"
    ),
    node(["datum"],
     lambda inp: datetime.datetime.now().strftime("%Y/%m/%d")
    ),
    node(["cas","hodin", "kolik je"],
     lambda inp: "právě je "+datetime.datetime.now().strftime("%H:%M:%S")
    ),
    node(["neopic"],
     lambda inp: inp,
     [
         node(["prosim"],
            lambda inp: "ok sry"
         )
     ]
    ),
    node(["s{3}"],
     lambda inp: "nope",
     useRegex=True
    ),
    node(["pomoc","co?"],
     lambda inp: print(Three)
    ),
    node(["co (.*) delas"],
     lambda inp, kw: "idk, " + str(kw[0][0]) + "?",
     useRegex=True
    )
    ]