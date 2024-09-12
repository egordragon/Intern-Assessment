from flask import render_template,request,redirect,url_for
from pymongo import MongoClient
from config.config import Config
from bson.objectid import ObjectId
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

def init_routes(app):
    """
    Initialize the routes for the todo app.
    Connect to MongoDB and set up endpoints for managing tasks.
    """
    client = MongoClient(os.environ.get('MONGO_URI'))  # Connect to the MongoDB instance using the configured URI
    db = client['todo_db']  # Access the database
    tasks_collection = db['tasks']  # Access the 'tasks' collection where tasks will be stored

    @app.route('/')
    def index():
        """
        Route to display all tasks.
        Retrieves tasks from the database and renders them on the 'index.html' template.
        """
        tasks = tasks_collection.find()  # Retrieve all tasks from the collection
        return render_template('index.html', tasks=tasks)  # Render tasks in the template

    @app.route('/', methods=['POST'])
    def add():
        """
        Route to add a new task.
        Retrieves the task from the form, stores it in the database with a default 'incomplete' status.
        """
        task = request.form['task']  # Get the task description from the submitted form
        created_at = datetime.now()  # Get the current timestamp
        tasks_collection.insert_one({
            'task': task, 
            'complete': False,  # By default, tasks are marked as incomplete
            'created_at': created_at  # Store when the task was created
        })
        return redirect(url_for('index'))  # Redirect to the index route to display all tasks

    @app.route('/toggle-complete/<task_id>', methods=['POST'])
    def toggle_complete(task_id):
        """
        Route to toggle the 'complete' status of a task.
        Updates the task's 'complete' field in the database.
        """
        task = tasks_collection.find_one({'_id': ObjectId(task_id)})  # Find the task by its id
        new_status = not task.get('complete', False)  # Toggle the 'complete' status
        tasks_collection.update_one(
            {'_id': ObjectId(task_id)}, 
            {'$set': {'complete': new_status}}  # Update the 'complete' status in the database
        )
        return redirect(url_for('index'))  # Redirect to the index route after updating

    @app.route('/delete/<task_id>', methods=['POST'])
    def delete(task_id):
        """
        Route to delete a task.
        Removes the task with the given id from the database.
        """
        tasks_collection.delete_one({'_id': ObjectId(task_id)})  # Delete the task by its id
        return redirect(url_for('index'))  # Redirect to the index route after deletion