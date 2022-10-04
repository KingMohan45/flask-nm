import os, json

import pytest

#import app from main.py
from main import app
from models import Todo, db

from .dummy_data import completed_tasks, incomplete_tasks

def insert_tasks():
    for task in completed_tasks:
        todo = Todo(task=task['task'], is_complete=task['is_complete'])
        db.session.add(todo)

    for task in incomplete_tasks:
        todo = Todo(task=task['task'], is_complete=task['is_complete'])
        db.session.add(todo)
    
    db.session.commit()


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['DEBUG'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            insert_tasks()

            yield client

            db.drop_all()

    # teardown
    os.remove('test.sqlite3')


def test_model(client):
    assert Todo.query.count() == 20
    assert Todo.query.filter_by(is_complete=True).count() == 10
    assert Todo.query.filter_by(is_complete=False).count() == 10
    

def test_health_check(client):
    response = client.get('/health-check')
    data = response.data.decode('UTF-8')

    assert response.status_code == 200
    assert response.data.decode('UTF-8') == 'OK'


def test_get_all(client):
    response = client.get('/get/all')
    data = response.data.decode('UTF-8')

    #tojson
    data = json.loads(data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['message'] == 'Tasks fetched successfully'
    assert len(data['data']) == 20


def test_get_all_tasks(client):
    response = client.get('/get/all')
    data = response.data.decode('UTF-8')

    #tojson
    data = json.loads(data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['message'] == 'Tasks fetched successfully'
    assert len(data['data']) == 20


def test_get_completed_tasks(client):
    response = client.get('/get/complete')
    data = response.data.decode('UTF-8')

    #tojson
    data = json.loads(data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['message'] == 'Tasks fetched successfully'
    assert len(data['data']) == 10


def test_get_incomplete_tasks(client):
    response = client.get('/get/incomplete')
    data = response.data.decode('UTF-8')

    #tojson
    data = json.loads(data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['message'] == 'Tasks fetched successfully'
    assert len(data['data']) == 10

def test_delete_task(client):
    #deleting a completed task
    response = client.delete('/delete/1')
    data = response.data.decode('UTF-8')

    #tojson
    data = json.loads(data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['message'] == 'Task deleted successfully'

    completed = Todo.query.filter_by(is_complete=True).count()
    assert completed == 9

def test_mark_task_complete(client):
    #marking an incomplete task as complete
    response = client.put('/mark/11/1')
    data = response.data.decode('UTF-8')

    #tojson
    data = json.loads(data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['message'] == 'Task updated successfully'

    completed = Todo.query.filter_by(is_complete=True).count()
    incomplete = Todo.query.filter_by(is_complete=False).count()
    
    assert completed == 11
    assert incomplete == 9

def test_mark_task_incomplete(client):
    #marking an incomplete task as complete
    response = client.put('/mark/1/0')
    data = response.data.decode('UTF-8')

    #tojson
    data = json.loads(data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['message'] == 'Task updated successfully'

    completed = Todo.query.filter_by(is_complete=True).count()
    incomplete = Todo.query.filter_by(is_complete=False).count()
    
    assert completed == 9
    assert incomplete == 11