import os
class Config:
    MONGO_URI =  'mongodb://mongo:27017'

class TestConfig(Config):
    MONGO_URI = 'mongodb://mongo:27017/todoapptest'
    TESTING = True