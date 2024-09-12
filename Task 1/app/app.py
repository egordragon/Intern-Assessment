from flask import Flask
from routes.routes import init_routes
from dotenv import load_dotenv

app = Flask(__name__,template_folder='templates')  #Initialize the Flask app and set the folder for templates
load_dotenv()
init_routes(app) # Initialize the app's routes

if __name__ == '__main__':
    app.run() # Start the Flask app