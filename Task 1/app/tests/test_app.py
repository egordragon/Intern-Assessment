import pytest
from pymongo import MongoClient
from bson.objectid import ObjectId
from app.config.config import TestConfig
from app.app import app


@pytest.fixture(scope='module')
def test_app():
    """
    Set up the Flask test app and test MongoDB configuration.
    The test database will be cleaned before and after each test module.
    """
    app.config.from_object(TestConfig)  # Load the test configuration
    app.template_folder = 'tests/templates'  # Set the template folder for testing

    # Initialize MongoDB client and drop collections for a clean test environment
    client = MongoClient(TestConfig.MONGO_URI)
    db = client['todo_db']
    db.drop_collection('tasks')  # Ensure tasks collection is empty before tests run

    yield app  # Provide the app to the tests

    # Clean up: drop the tasks collection after tests are done
    db.drop_collection('tasks')

@pytest.fixture(scope='module')
def client(test_app):
    """
    Set up a test client using the test Flask app.
    """
    return test_app.test_client()

def test_index(client):
    """
    Test the index route by adding a task and checking the response.
    """
    # Add a task to the database for testing
    client.post('/', data={'task': 'Test Task'})

    # Access the index route
    response = client.get('/')

    # Assert the response status and that the task appears on the page
    assert response.status_code == 200
    assert b'Test Task' in response.data  # Check if 'Test Task' is in the response HTML

def test_add_task(client):
    """
    Test the task addition functionality.
    """
    # Post a new task
    response = client.post('/', data={'task': 'Add Task Test'})

    # Check if the app redirects after adding the task (expected behavior)
    assert response.status_code == 302  # 302 indicates a redirect (typically to the index page)

    # Confirm that the task appears in the task list
    response = client.get('/')
    assert b'Add Task Test' in response.data  # Ensure the new task is present
    assert b'Incomplete' in response.data  # Ensure the task is marked as incomplete by default

def test_toggle_complete(client):
    """
    Test toggling the completion status of a task.
    """
    # Add a task for toggling
    response = client.post('/', data={'task': 'Toggle Test Task'})
    assert response.status_code == 302  # Confirm that task addition succeeds

    # Retrieve the task from the database
    mongo_client = MongoClient(TestConfig.MONGO_URI)
    db = mongo_client['todo_db']
    task = db['tasks'].find_one({'task': 'Toggle Test Task'})
    task_id = str(task['_id'])  # Get the task's MongoDB ObjectId

    # Toggle the completion status of the task
    response = client.post(f'/toggle-complete/{task_id}')
    assert response.status_code == 302  # Ensure the toggle request redirects

    # Verify that the task is now marked as complete
    updated_task = db['tasks'].find_one({'_id': ObjectId(task_id)})
    assert updated_task['complete'] is True  # Task should be marked complete after toggle

    # Toggle the task back to incomplete
    response = client.post(f'/toggle-complete/{task_id}')
    assert response.status_code == 302  # Check redirection again
    updated_task = db['tasks'].find_one({'_id': ObjectId(task_id)})
    assert updated_task['complete'] is False  # Task should be incomplete again

def test_delete_task(client):
    """
    Test task deletion functionality.
    """
    # Add a task for deletion testing
    response = client.post('/', data={'task': 'Delete Test Task'})
    assert response.status_code == 302  # Ensure task addition works

    # Retrieve the task from the database
    mongo_client = MongoClient(TestConfig.MONGO_URI)
    db = mongo_client['todo_db']
    task = db['tasks'].find_one({'task': 'Delete Test Task'})
    task_id = str(task['_id'])  # Get the task's MongoDB ObjectId

    # Delete the task
    response = client.post(f'/delete/{task_id}')
    assert response.status_code == 302  # Confirm the app redirects after deletion

    # Verify that the task is deleted from the database
    deleted_task = db['tasks'].find_one({'_id': ObjectId(task_id)})
    assert deleted_task is None  # Task should no longer exist