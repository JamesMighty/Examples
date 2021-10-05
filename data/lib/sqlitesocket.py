import atexit
from sqlite3.dbapi2 import Connection
from data.lib.sqlquery import SqlQuery, TableSqlQuery


class SqliteSocket(Connection):
    """
    Expands sqlite3 connection api
    """
    def __init__(self, db_path:str):
        """
        Args:
            db_path (str): path to database file
        """
        super().__init__(db_path)
        self._db_path = db_path
        self.is_open = True
        atexit.register(self.close)
    
    @property
    def cursor(self):
        """
        Returns new cursor.
        """
        return super().cursor()
    
    @property
    def query(self):
        return SqlQuery(self)

    def close(self):
        """
        If socket is alive, commits transactions and closes connection.\n
        Natively called at program exit.
        """
        if self.is_open:
            self.save()
            self.close()
            self.is_open = False
    
    def discard(self):
        """
        If socket is alive, closes connection without commiting transactions.\n
        """
        if self.is_open:
            self.close()
            self.is_open = False
    
    def save(self):
        """
        If socket is still alive, commits executed transactions.
        """
        if self.is_open:
            self.commit()
class sqliteTableSocket(SqliteSocket):

    """[summary]\n
    Defines sqlite socket for specified table in db file.\n
    If the table does not exist, create one.
    """
    def __init__(self, db_path:str, table_name:str, table_scheme:str) -> None:
        super().__init__(db_path)
        self.table_name = table_name
        self.table_scheme = table_scheme
        SqlQuery(self).create_table_if_not_exists(self.table_name,self.table_scheme).execute()
        self.save()
    
    @property
    def query(self):
        return TableSqlQuery(self)
    
    