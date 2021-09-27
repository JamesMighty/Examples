import atexit
import sqlite3


class sqliteTableSocket:

    def __init__(self, db_path, table_name, items_buffer_count:int=10) -> None:
        self._db_path = db_path
        self._is_connected = False
        self._items_buffer_count = items_buffer_count
        self._request_count = 0
        self.table_name = table_name
        
        self._dbconnection = sqlite3.connect(db_path)
        self._cursor = self._dbconnection.cursor()
        self._is_connected = True
        self._create_table_if_not_exist()
        self.save()

        atexit.register(self.discard)
    
    def _create_table_if_not_exist(self):
        query = f'''CREATE TABLE IF NOT EXISTS {self.table_name} (ID INTEGER PRIMARY KEY,Key TEXT NOT NULL,Value BLOB,table_constraints)'''
        self._cursor.execute(query)

    def _next_request(self):
        self._request_count+=1
        if self._request_count == self._items_buffer_count:
            self.save()
            self._request_count = 0
    
    def discard(self):
        if self._is_connected:
            self.save()
            self._dbconnection.close()
            self._is_connected = False
    
    def save(self):
        if self._is_connected:
            self._dbconnection.commit()
    