from data.lib.datastore.context import Context


class Command:
    def __init__(self, commandCall=None) -> None:
        if commandCall is not None:
            self.__call__ = commandCall
        pass

    def __call__(self, context: Context, query: str, **kwargs) -> str:
        raise NotImplementedError()