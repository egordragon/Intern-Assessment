from flask import Flask
from routes.routes import init_routes

app = Flask(__name__,template_folder='templates')  #Initialize the Flask app and set the folder for templates
init_routes(app) # Initialize the app's routes

if __name__ == '__main__':
    port = 8080
    app.run(host='0.0.0.0', port=port ) # Start the Flask app