from data.lib.sqlitesocket import sqliteTableSocket
from typing import Any, Iterator, Union
from data.lib.datastore.datastore import Datastore
import sqlite3
import pickle
import atexit

class sqliteDatastore(Datastore, sqliteTableSocket):

    def __init__(self, db_path, table_name, items_buffer_count:int=10, payload: dict={}, create_meta: bool=True) -> None:
        super().__init__(payload=payload, create_meta=create_meta)
        sqliteTableSocket.__init__(self,db_path,table_name,items_buffer_count)
    
    def __getitem__(self, k) -> Union['Datastore', Any]:
        if self._is_connected:
            query = f"SELECT Value from {self.table_name} WHERE Key='{k}'"
            response = self._cursor.execute(query).fetchone()
            data = pickle.loads(response[0])
            return data
        else:
            return None
    
    def __setitem__(self, k: str, v: Any) -> None:
        if self._is_connected:
            query = f"SELECT Value from {self.table_name} WHERE Key='{k}'"
            response = self._cursor.execute(query).fetchone()
            pickled_data = (pickle.dumps(v))
            if not response:
                self._cursor.execute(f"INSERT INTO {self.table_name} (Key, Value) VALUES ('{k}',?)", (pickled_data,))
            else:
                self._cursor.execute(f"UPDATE {self.table_name} SET Value=? WHERE Key='{k}'", (pickled_data,))
            self._next_request()

    def __delitem__(self, v: Any) -> None:
        response = self._cursor.execute(f"DELETE FROM {self.table_name} WHERE Key='{v}'")
        self._next_request()
    
    def __iter__(self) -> 'sqliteDatastoreIterator':
        return sqliteDatastoreIterator(self._db_path, self.table_name)


class sqliteDatastoreIterator(sqliteTableSocket,Iterator):

    def __init__(self, db_path:str, table:str, start:int=0, stop:int=None, order_by:str=None, items_buffer_count:int=10) -> None:
        super().__init__(db_path,table,items_buffer_count)
        self._counter = 0
    
    def __iter__(self) -> Iterator[Any]:
        return self
    
    def __next__(self) -> Any:
        query = f"SELECT Key,Value from {self.table_name} LIMIT 1 OFFSET {self._counter}"
        response = self._cursor.execute(query).fetchone()
        if response:
            data = pickle.loads(response[1])
            self._counter += 1
            return (response[0],data)
        raise StopIteration