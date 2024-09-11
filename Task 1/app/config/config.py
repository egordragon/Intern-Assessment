class Config:
    MONGO_URI = 'mongodb://mongo:27017/todoapp'

class TestConfig(Config):
    MONGO_URI = 'mongodb://mongo:27017/todoapptest'
    TESTING = True
MONGO_URI = 'mongodb://todo_db:27017/todoapp'   