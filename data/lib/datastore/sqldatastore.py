import atexit
from data.lib.sqlquery import SqlQuery
import pickle
import sqlite3
from typing import Any, Callable, Iterator, Union

from data.lib.datastore.datastore import Datastore
from data.lib.sqlitesocket import sqliteTableSocket


class SqliteDatastore(Datastore):

    TABLE_SCHEMA = "ID INTEGER PRIMARY KEY,Key TEXT NOT NULL,Value {ValueType}"

    def __init__(self, 
                 db_path:str,
                 table_name:str,
                 payload:dict = {},
                 create_meta:bool = True,
                 object_wrapper:Callable[[Any], Union[str,bytes]]=pickle.dumps,
                 object_unwrapper:Callable[[Union[str,bytes]], Any]=pickle.loads
                ):
        self.wrapper = object_wrapper
        self.value_unwrapper = object_unwrapper
        vtype = self._get_value_type_from_wrapper()
        print(f"SqliteDatastore: table value type will be '{vtype}'")
        table_schema = self.TABLE_SCHEMA.format(ValueType=vtype)
        self.db = sqliteTableSocket(db_path, table_name, table_schema)
        super().__init__(payload=payload, create_meta=create_meta)
        
    
    def _get_value_type_from_wrapper(self) -> str:
        try:
            ret = self.wrapper.__annotations__["return"]
            print(f"return annotation for '{self.wrapper}' is '{ret}'")
            if issubclass(ret,int):
                return "INTEGER"
            elif issubclass(ret,float):
                return "REAL"
            elif issubclass(ret,str):
                return "TEXT"
            elif issubclass(ret,bytes):
                return "BLOB"
        except Exception:
            return "BLOB"

    def __getitem__(self, k) -> Union['Datastore', Any]:
        if self.db.is_open:
            response = self.db.query.select("Value").where(Key=k).execute().fetchone()
            data = self.value_unwrapper(response[0])
            return data
        else:
            return None

    def __setitem__(self, k: str, v: Any) -> None:
        if self.db.is_open:
            response = self.db.query.select("Value").where(Key=k).execute().fetchone()
            pickled_data = self.wrapper(v)
            if not response:
                self.db.query.insert(Key=k,Value=pickled_data).execute()
            else:
                self.db.query.update(Value=pickled_data).where(Key=k).execute()

    def __delitem__(self, v: Any) -> None:
        self.db.query.delete().where(Key=v).execute()

    def __iter__(self) -> 'SqliteDatastoreIterator':
        return SqliteDatastoreIterator(self)


class SqliteDatastoreIterator(Iterator):
    COLUMNS_SELECTOR = "Key,Value"

    def __init__(self, sqlite_datastore: SqliteDatastore) -> None:
        self.datastore = sqlite_datastore
        self._counter = 0

    def __iter__(self) -> Iterator[Any]:
        return self

    def __next__(self) -> Any:
        response = self.datastore.db.query.select(SqliteDatastoreIterator.COLUMNS_SELECTOR).limit(1).offset(self._counter).execute().fetchone()
        if response:
            data = self.datastore.value_unwrapper(response[1])
            self._counter += 1
            return response[0], data
        raise StopIteration
