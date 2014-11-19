import fields
import models
import query
import pymongo

class Session(object):
    def __init__(self, host, port, dbname = None):
        self._conn = pymongo.Connection(host = host, port = port)
        self._db = None
        if dbname is not None:
            self.use(dbname)

    def close(self):
        self._conn.close()

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.close()

    def use(self, dbname):
        self._db = self._conn[dbname]
        return self

    @property
    def conn(self):
        return self._conn

    @property
    def db(self):
        return self._db

    def query(self, model_cls, *fields):
        return query.Query(self._db, model_cls, fields)

    def delete(self, model):
        collection = self._db[model.__class__.collection_name()]
        bson_data = model.__class__.to_bson_data(model)
        return collection.remove(bson_data, getLastErr = True)
        
    def add(self, model):
        bson_data = model.__class__.to_bson_data(model)
        if '_id' in bson_data:
            del bson_data['_id']
        collection = self._db[model.__class__.collection_name()]
        return collection.save(bson_data, getLastErr = True)
        
    def save(self, model):
        bson_data = model.__class__.to_bson_data(model)
        collection = self._db[model.__class__.collection_name()]
        return collection.save(bson_data, getLastErr = True)
