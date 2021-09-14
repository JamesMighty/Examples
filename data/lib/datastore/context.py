from data.lib.datastore.datastore import Datastore, DatastoreProvider
from data.lib.datastore.sqldatastore import sqliteDatastore


class Context(Datastore):

    def __init__(self, iterable=(), **kwargs):
        super().__init__(self)
        self.update(iterable,**kwargs)
    

class ContextProvider(DatastoreProvider):

    def __init__(self, payload={}) -> None:
        self._context = Context(payload)
    
    @property
    def context(self) -> Context:
        return self._context    


class sqliteContext(sqliteDatastore):

    def __init__(self, db_path:str, table_name:str, payload: dict={}, create_meta: bool=True) -> None:
        super().__init__(db_path, table_name, payload=payload, create_meta=create_meta)

