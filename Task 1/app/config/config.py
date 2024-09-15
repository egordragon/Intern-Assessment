import os
class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://Egor:todoapp@cluster0.icjoqn4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

class TestConfig(Config):
    MONGO_URI = 'mongodb://mongo:27017/todoapptest'
    TESTING = True