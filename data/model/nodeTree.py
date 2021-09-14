# -*- coding: utf-8 -*-
from data.resources.node import *
import datetime
import data.api.userAPI as uapi

global RootThree
RootTree = [
    Node(["ahoj","cus","cau", "nazdar"],
        lambda setx, inp: "nazdar",
        [
            Node(["se mas", "ti je"], 
                lambda setx, inp: "mám se celkem fajn"
            )
        ]
    ),
    Find(["pls"],
        [
            Node(["se mas"],
                lambda setx, inp: "naprosto skvěle"
            ),
            DoOnlyOne([
                Node(["nemluv","mlc"],
                    lambda setx, inp: uapi.switch_tts(setx,False)
                ),
                Node(["mluv"],
                    lambda setx, inp: uapi.switch_tts(setx,True)
                )
            ])
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
        lambda setx, inp: "právě je "+datetime.datetime.now().strftime("%H:%M")
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
        lambda setx, inp: uapi.get_help(RootTree),
        desiredEnd="",
    ),
    RegexNode(["co (.*) delas"],
        lambda setx, inp, kw: "idk, " + str(kw[0][0]),
        desiredEnd="?"
    ),
    Find(["zmen", "uprav"],
        [
            DoOnlyOne([
                RegexNode(["format na '(.*)'"],
                    lambda setx, inp, kw: uapi.change_output_format(setx, format=kw[0][0]),
                ),
                Node(["format"],
                    lambda setx, inp: uapi.change_output_format(setx)
                )
            ]),
            DoOnlyOne([
                RegexNode(["jmeno na '(.*)'"],
                    lambda setx, inp, kw: uapi.change_username(setx, username=kw[0][0]),
                ),
                Node(["jmeno"],
                    lambda setx, inp: uapi.change_username(setx)
                )
            ])
        ]
    ),
    Find(["muzes", "umis", "dokazes"],
    [
        Node(["mluvit"],
            lambda setx, inp: uapi.get_context_answer_for_settings(setx, "DoSpeak")
        )
    ]
    )
    ]