import os
class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongo:27017/todo_db')

class TestConfig(Config):
    MONGO_URI = 'mongodb://mongo:27017/todoapptest'
    TESTING = True