from flags import Flags
import sqlite3
import data.lib.utility as utils


class SqlStatementTypes(Flags):
    MAIN = 2
    CONDITION = 4
    ADDITIONAL = 8
    END = 16


class SqlQuery:

    def __init__(self) -> None:
        self._query = ""
        self._statements = []
        self._cursor = -1
        pass

    def select(self, _selector, _from):
        self._statements.append([(SqlStatementTypes.MAIN, f"SELECT {_selector} FROM {_from} ")])
        self._cursor = len(self._statements)-1
        return self

    def where(self, _where):
        self._statements[self._cursor].append((SqlStatementTypes.CONDITION, f"WHERE {_where} "))
        return self

    def create_table(self, _name, _scheme):
        self._statements.append([(SqlStatementTypes.MAIN, f"CREATE TABLE {_name} ({_scheme}) ")])
        self._cursor = len(self._statements)-1
        return self

    def limit(self, _limit):
        self._statements[self._cursor].append((SqlStatementTypes.ADDITIONAL, f"LIMIT {_limit} "))
        return self

    def offset(self, _offset):
        self._statements[self._cursor].append((SqlStatementTypes.ADDITIONAL, f"OFFSET {_offset} "))
        return self

    def create_table_if_not_exists(self, _name, _scheme):
        self._statements.append([(SqlStatementTypes.MAIN, f"CREATE TABLE IF NOT EXISTS {_name} ({_scheme}) ")])
        self._cursor = len(self._statements)-1
        return self

    def compose(self):
        for list in self._statements:
            list.sort(key=lambda tuple: int(tuple[0]))
            if SqlStatementTypes.MAIN in [tuple[0] for tuple in list]:
                list.append((SqlStatementTypes.END,";"))
        #print(self._statements)
        proc = utils.flatten(self._statements)
        #print(proc)
        words = [statement[1] for statement in proc]
        #print(words)
        self._query = " ".join(words)

    def flush(self):
        self.compose()
        query = self._query
        self._query = ""
        return query       

    def check(self, _db_path=":memory:"):

        temp_db = sqlite3.connect(_db_path)

        try:
            temp_db.execute(self._query)
            return True
        except Exception as e:
            print(f"Bad query: {e}")
            return False
        finally:
            temp_db.close()
