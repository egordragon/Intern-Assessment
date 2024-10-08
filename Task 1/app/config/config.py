import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongo:27017/todo_db')

class TestConfig(Config):
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongo:27017/todo_db_test')
    TESTING = True