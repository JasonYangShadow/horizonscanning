from pymongo import MongoClient
from pprint import pprint
from config import Config
from exception import Type, TeleException
from crypto import Crypto
from bson import ObjectId


class Mongo:
    def __init__(self, config_path=None):
        if config_path is None:
            self.__config = Config()
        else:
            self.__config = Config(config_path)
            self.__host = self.__config.getValue('Mongo', 'HOST')
            self.__port = self.__config.getValue('Mongo', 'PORT')
            self.__cry = Crypto()
            self.__user = self.__cry.decrypt(
                    self.__config.getValue('Mongo', 'USER')).decode("utf-8")
            self.__pass = self.__cry.decrypt(
                    self.__config.getValue('Mongo', 'PASS')).decode("utf-8")
            self.__database = self.__config.getValue('Mongo', 'DATABASE')
            #connection_str="mongodb://"+self.__user+":"+self.__pass+"@"+self.__host+":"+self.__port+"/?authSource=admin"
            connection_str = "mongodb://" + self.__user + ":" + self.__pass + "@" + self.__host + ":" + self.__port + "/" + self.__database
            self.__client = MongoClient(connection_str, maxPoolSize=200, waitQueueTimeoutMS=100)
            self.__db = None

    def getDB(self, database):
        self.__db = self.__client[database]
        return self.__db

    def getCollection(self, collection):
        if self.__db is None:
            self.getDB(self.__database)
        self.__collection = self.__db[collection]
        return self.__collection

    def insert(self, record, collection):
        if not isinstance(record, list):
            raise TeleException(Type.WrongTypeException,
                    'record should be list')
            self.getCollection(collection)
        return self.__collection.insert_many(record).inserted_ids

    def find(self, collection, condition=None):
        if condition is not None and not isinstance(condition, dict):
            raise TeleException(Type.WrongTypeException,
                    'condition should be dict type')
            self.getCollection(collection)
        if condition is None:
            return list(self.__collection.find())
        else:
            return list(self.__collection.find(condition))

    def findSkipLimit(self, collection, skip, limit, condition=None):
        if condition is not None and not isinstance(condition, dict):
            raise TeleException(Type.WrongTypeException,
                    'condition should be dict type')
            self.getCollection(collection)
        if condition is None:
            return list(self.__collection.find().skip(skip).limit(limit))
        else:
            return list(self.__collection.find(condition).skip(skip).limit(limit))

    def count(self,collection,condition=None):
        if condition is not None and not isinstance(condition, dict):
            raise TeleException(Type.WrongTypeException,
                    'condition should be dict type')
            self.getCollection(collection)
        if condition is None:
            return self.__collection.find().count()
        else:
            return self.__collection.find(condition).count()

    def exist(self, condition, collection):
        if not isinstance(condition, dict):
            raise TeleException(Type.WrongTypeException,
                    'condition should be dict type')
            self.getCollection(collection)
        return True if self.__collection.count(condition) > 0 else False

    def update(self, condition, update, collection):
        if not isinstance(condition, dict):
            raise TeleException(Type.WrongTypeException,
                    'condition should be dict')
            if not isinstance(update, dict):
                raise TeleException(Type.WrongTypeException,
                        'update should be dict')
                self.getCollection(collection)
        return self.__collection.update_many(condition, update)

    def saveUpdate(self, condition, update, collection):
        if not isinstance(condition, dict):
            raise TeleException(Type.WrongTypeException,
                    'condition should be dict')
            if not isinstance(update, dict):
                raise TeleException(Type.WrongTypeException,
                        'update should be dict')
                self.getCollection(collection)
        return self.__collection.update_many(condition, update, True)

    def saveUpdateOne(self, condition, update, collection):
        if not isinstance(condition, dict):
            raise TeleException(Type.WrongTypeException,
                    'condition should be dict')
            if not isinstance(update, dict):
                raise TeleException(Type.WrongTypeException,
                        'update should be dict')
                self.getCollection(collection)
        return self.__collection.update_one(condition, update, True)

    def deleteMany(self, idList, collection):
        if not isinstance(idList, list):
            raise TeleException(Type.WrongTypeException,
                    'idList should be list')
            self.getCollection(collection)
        for obj in idList:
            self.__collection.delete_one({'_id': ObjectId(obj)})
