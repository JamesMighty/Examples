from data.lib.datastore.sqldatastore import SqliteDatastore

datastore = SqliteDatastore("data/model/context.db", "sandbox")
print(datastore["ahoj"])
datastore.save()