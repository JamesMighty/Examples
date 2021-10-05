from unicodedata import name
from data.lib.datastore.datastore import Datastore, DatastoreRootProvider, DatastoreSubscriber
from data.lib.datastore.sqldatastore import SqliteDatastore


class Context(Datastore):

    def __init__(self, payload={}, **kwargs):
        super().__init__(self)
        self.update(payload,**kwargs)
    

class ContextRootProvider(DatastoreRootProvider):

    def __init__(self, payload={}) -> None:
        self._datastore = Context(payload)
    
    @DatastoreRootProvider.datastore.getter
    def context(self) -> Context:
        return self._datastore    
    

class ContextSubscriber(DatastoreSubscriber):

    def __init__(self, id:str=None) -> None:
        super().__init__(id=id)

    
    @DatastoreSubscriber.datastore.getter
    def subscribedContext(self) -> Context:
        return self._provider.datastore[self.id]
    
    @DatastoreSubscriber.parent_datastore.getter
    def parentContext(self) -> Context:
        return self._provider.datastore


class sqliteContext(SqliteDatastore):

    def __init__(self, db_path:str, table_name:str, payload: dict={}, create_meta: bool=True) -> None:
        super().__init__(db_path, table_name, payload=payload, create_meta=create_meta)

