from flags import Flags
import sqlite3
from data.lib.sqlitesocket import sqliteTableSocket
import data.lib.utility as utils

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sqlite3.dbapi2 import Cursor
    from data.lib.sqlitesocket import SqliteSocket


class SqlStatementTypes(Flags):
    MAIN = 2
    CONDITION = 4
    ADDITIONAL = 8
    END = 16


class SqlQuery:

    def __init__(self, connection:'SqliteSocket') -> None:
        self._query = ""
        self._vars = []
        self._statements = [[]]
        self._stm_cursor = 0
        self._connection = connection

    def compose(self):
        for main_st_list in self._statements:
            main_st_list.sort(key=lambda tuple: int(tuple[0]))
            if SqlStatementTypes.MAIN in [tuple[0] for tuple in main_st_list]:
                main_st_list.append((SqlStatementTypes.END,";",()))
        # print(self._statements)
        proc = utils.flatten(self._statements)
        # print(proc)
        types, words, vars = zip(*proc)
        # print(words)
        self._vars = utils.flatten(vars)
        # print(self._vars)
        self._query = " ".join(words)

    def flush(self):
        self.compose()
        query = self._query
        self._query = ""
        self._statements = []
        return query       
    
    def execute(self) -> 'Cursor':
        self.compose()
        response = self._connection.cursor.execute(self._query, self._vars)
        return response

    def check(self) -> bool:

        temp_db = sqlite3.connect(self._connection._db_path)

        try:
            temp_db.execute(self._query)
            return True
        except Exception as e:
            print(f"Bad query: {e}")
            return False
        finally:
            temp_db.close()

    def select(self, _selector:str, _from:str, *vars):
        self._statements.append([(SqlStatementTypes.MAIN, f"SELECT {_selector} FROM {_from} ", vars)])
        self._stm_cursor = len(self._statements)-1
        return self
    
    def delete(self, _from:str, *vars):
        self._statements.append([(SqlStatementTypes.MAIN, f"DELETE FROM {_from} ", vars)])
        self._stm_cursor = len(self._statements)-1
        return self
    
    def insert(self, _into:str, **kvars ):
        names = kvars.keys()
        values = kvars.values()
        valstr = ",".join(["?"]*len(values))
        self._statements.append([(SqlStatementTypes.MAIN, f"INSERT INTO {_into} ({','.join(names)}) VALUES ({valstr})", values)])
        self._stm_cursor = len(self._statements)-1
        return self
    
    def update(self, _table:str, **kvars ):
        names = kvars.keys()
        values = kvars.values()
        valstr = ", ".join([f"{name}=?" for name in names])
        self._statements.append([(SqlStatementTypes.MAIN, f"UPDATE {_table} SET {valstr}", values)])
        self._stm_cursor = len(self._statements)-1
        return self

    def where(self, **kvars):
        names = kvars.keys()
        vars = kvars.values()
        valstr = ",".join([f"{name}=?" for name in names])
        self._statements[self._stm_cursor].append((SqlStatementTypes.CONDITION, f"WHERE {valstr} ", vars))
        return self

    def create_table(self, _name, _scheme, *vars):
        self._statements.append([(SqlStatementTypes.MAIN, f"CREATE TABLE {_name} ({_scheme}) ", vars)])
        self._stm_cursor = len(self._statements)-1
        return self

    def limit(self, _limit, *vars):
        self._statements[self._stm_cursor].append((SqlStatementTypes.ADDITIONAL, f"LIMIT {_limit} ",vars))
        return self

    def offset(self, _offset, *vars):
        self._statements[self._stm_cursor].append((SqlStatementTypes.ADDITIONAL, f"OFFSET {_offset} ", vars))
        return self

    def create_table_if_not_exists(self, _name, _scheme, *vars):
        self._statements.append([(SqlStatementTypes.MAIN, f"CREATE TABLE IF NOT EXISTS {_name} ({_scheme}) ", vars)])
        self._stm_cursor = len(self._statements)-1
        return self
    
    def next(self):
        self._statements[self._stm_cursor].append((SqlStatementTypes.END,";",()))

class TableSqlQuery(SqlQuery):

    def __init__(self, table_socket:sqliteTableSocket):
        super().__init__(table_socket)
        self.table = table_socket

    def select(self, _selector:str, *vars) -> 'TableSqlQuery':
        return super().select(self, _selector, self.table.table_name, *vars)   
    
    def insert(self, **kvars) -> 'TableSqlQuery':
        return super().insert(self, self.table.table_name, **kvars)

    def update(self, **kvars) -> 'TableSqlQuery':
        return super().update(self.table.table_name, **kvars)
    
    def delete(self, *vars) -> 'TableSqlQuery':
        return super().delete(self.table.table_name, *vars)