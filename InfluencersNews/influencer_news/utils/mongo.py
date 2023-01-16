import pymongo
from utils.utils import printAndLog, printAndLogError


class Mongo:

    '''
    Mongo init functions, given the logfile set logfile name
    '''
    def __init__(self, logfile, collection_log):
        self.logfile_name = logfile
        self.collection_log = collection_log
    

    '''
    Given a connection string:
    - connect to mongo
    - set mongo client
    '''
    def connect(self, args):
        try:
            printAndLog(self.logfile_name, "[*] mongo.connect(connection_string)")
            connection_string = args[0]
            self.mongo_client = pymongo.MongoClient(connection_string, serverSelectionTimeoutMS=1)
            self.mongo_client.server_info() 
        except Exception as e:
            printAndLogError(self.logfile_name, "[-] mongo.connect(connection_string) - error message: {}".format(str(e)))
            return -1
    

    '''
    Set DB
    '''
    def setDB(self, args):
        try:
            printAndLog(self.logfile_name, "[*] mongo.setDB(self, db_name)")
            db_name = args[0]
            self.db = self.mongo_client[db_name]
            return 0
        except Exception as e:
            printAndLogError(self.logfile_name, "[-] mongo.setDB(self, db_name) - error message: {}".format(str(e)))
            return -1


    '''
    Given collection names and an array write many in mongo
    '''
    def writeMany(self, args):
        try: 
            printAndLog(self.logfile_name, "[*] mongo.writeMany(collection_name, array)")
            collection_name = args[0]
            array = args[1]
            collection = self.db[collection_name]
            collection.insert_many(array)
            return 0
        except Exception as e:
            printAndLogError(self.logfile_name, "[-] mongo.writeMany(collection_name, array) - error message: {}".format(str(e)))
            return -1
    

    '''
    Given a collection names and an object write once in mongo
    '''
    def writeOnce(self, args):
        try: 
            printAndLog(self.logfile_name, "[*] mongo.writeOnce(collection_name, obj)")
            collection_name = args[0]
            obj = args[1]
            collection = self.db[collection_name]
            collection.insert_one(obj)
            return 0
        except Exception as e:
            printAndLogError(self.logfile_name, "[-] mongo.writeOnce(collection_name, obj) - error message: {}".format(str(e)))
            return -1
    

    '''
    WriteOnce wrapper to insert a single log in the collection self.collection_log: required in input mode, action and acquisition datetime 
    '''
    def writeLog(self, args):
        try: 
            printAndLog(self.logfile_name, "[*] mongo.writeLog(mode, action, state, acquisition_time)")
            mode = args[0]
            action = args[1]
            acquisition_time = args[2]
            return self.writeOnce([self.collection_log, {"mode":mode,"action":action, "datetime":acquisition_time}])
        except Exception as e:
            printAndLogError(self.logfile_name, "[-] mongo.writeLog(mode, action, state, acquisition_time) - error message: {}".format(str(e)))
            return -1
    

    '''
    Given a query find in the self.collection_log collection the latest log 
    '''
    def findLastLog(self, args):
        try: 
            printAndLog(self.logfile_name, "[*] mongo.findLastLog(query)")
            query = args[0]
            collection = self.db[self.collection_log]
            return collection.find_one(query, sort=[("datetime",pymongo.DESCENDING)]) 
        except Exception as e:
            printAndLogError(self.logfile_name, "[-] mongo.findLastLog(collection_name, query, sort) - error message: {}".format(str(e)))
            return -1
    

    '''
    Given a collection names return all documents
    '''
    def find(self, args):
        try: 
            printAndLog(self.logfile_name, "[*] mongo.find(collection_name)")
            collection_name = args[0]
            collection = self.db[collection_name]
            return list(collection.find())
        except Exception as e:
            printAndLogError(self.logfile_name, "[-] mongo.find(collection_name) - error message: {}".format(str(e)))
            return -1

    '''
    Given a collection and an username return all related document 
    '''
    def getUserData(self, args):
        try: 
            printAndLog(self.logfile_name, "[*] mongo.getUserData(collection_name, name)")
            collection_name = args[0]
            username = args[1]
            collection = self.db[collection_name]
            return list(collection.find({"username":username}))
        except Exception as e:
            printAndLogError(self.logfile_name, "[-] mongo.getUserData(collection_name, name) - error message: {}".format(str(e)))
            return -1