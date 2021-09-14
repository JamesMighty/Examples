from data.resources.sqldatastore import sqliteDatastore

datastore = sqliteDatastore("data/model/context.db","sandbox")
print(datastore["ahoj"])
datastore.save()