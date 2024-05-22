import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


from pymongo import MongoClient
connection_string = "mongodb+srv://shahiddar:xrsVM8oLZM0p0JhK@cluster0.setxhtj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(connection_string)
db = client['db_name']


class Config():
  
    DATABASE = {
        
    }
    ENGINE  = 'djongo'
    MONGO_DB = 'buyhatke'
    MONGO_PORT = 27017
    MONGO_USER = 'shahidshabir'
    MONGO_PASSWORD = '123456'
    MONGO_DB_TEST = 'mdtest'
    BASE_URL = 'http://localhost:8000/'
    DEFAULT_CC_EMAILS = []
    ENV = 'local'

    MONGO_CONNECTION = "mongodb://localhost:27017/buyhatke"