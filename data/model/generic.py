from data.lib.datastore.context import Context
from data.lib.datastore.historycontext import (HistoryContext,
                                               sqliteHistoryContext)

DEFAULT_CONTEXT = Context({
                "AIName": "May",
                "indexation":"->",
                "username": None,
                "padding": 0,
                "DoSpeak": False,
                "_history": sqliteHistoryContext("data/model/context.db","may_mk1_history")
            })
