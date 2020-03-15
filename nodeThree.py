from command import node
import datetime

global Three
Three = [
    node(["ahoj","cus"],
     lambda inp: "nazdar", # odstraneni print()
     [
         node(["se mas", "ti je"],
          lambda inp: "mam se celkem fajn"
         )
     ]
    ),
    node(["se mas","ti je"],
     lambda inp: "na prd"
    ),
    node(["datum"],
     lambda inp: datetime.datetime.now().strftime("%Y/%m/%d")
    ),
    node(["cas","hodin", "kolik je"],
     lambda inp: "prave je "+datetime.datetime.now().strftime("%H:%M:%S")
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
     lambda inp: "nope"
    ),
    node(["pomoc","co?"],
     lambda inp: print(Three)
    )
    ]