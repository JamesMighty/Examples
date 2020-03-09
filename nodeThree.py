from command import node

global Three
Three = [
    node(["ahoj","cus"],
     lambda inp: print("nazdar"),
     [
         node(["se mas", "ti je"],
          lambda inp: print("mam se celkem fajn")
         )
     ]
    ),
    node(["se mas","ti je"],
     lambda inp: print("na prd")
    ),
    node(["datum"],
     lambda inp: print(datetime.datetime.now().strftime("%Y/%m/%d"))
    ),
    node(["cas","hodin", "kolik je"],
     lambda inp: print("prave je "+datetime.datetime.now().strftime("%H:%M:%S"))
    ),
    node(["neopic"],
     lambda inp: print(inp),
     [
         node(["prosim"],
            lambda inp: [print("ok, sorry"),inp][-0]
         )
     ]
    ),
    node(["s{3}"],
     lambda inp: print("nope")
    ),
    node(["pomoc","co?"],
     lambda inp: print( "\n".join([str(tupl[0]) for tupl in Three]))
    )
    ]