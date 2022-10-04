from flask import render_template, request, redirect, url_for, jsonify

from core import app
from models import Todo, db
from utils import api_response


@app.route('/health-check', methods=['GET'])
def health_check():
    return 'OK'


@app.route('/', methods=['GET'])
def home():
    #call /get/all route and get the data
    complete = data = get('complete').json.get('data')
    incomplete = get('incomplete').json.get('data')
    return render_template('home.html', incomplete=incomplete, complete=complete)


@app.route('/add', methods=['POST'])
def add():
    """
    This function is used to add a new task
    """
    task = request.form.get('task', None)

    if not task:
        return redirect(url_for('home', message='Task is required'))
    todo = Todo(task=task, is_complete=False)
    db.session.add(todo)
    db.session.commit()
    
    #redirect and pass message
    return redirect(url_for('home', message='Task added successfully'))


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    """
    This function is used to delete a task
    """

    task = Todo.query.filter_by(id=id).first()
    if not task:
        return api_response(None, message="No such task found", status=False, status_code=400)
    
    db.session.delete(task)
    db.session.commit()

    return api_response(None, message="Task deleted successfully", status=True, status_code=200)


@app.route('/mark/<int:id>/<int:status>', methods=['PUT'])
def mark(id, status):
    """
    Marks the given task with given status
    """
    task = Todo.query.filter_by(id=id).first()
    if not task:
        return api_response(None, message="No such task found", status=False, status_code=400)
    
    task.is_complete = True if status == 1 else False
    db.session.commit()

    return  api_response(None, message="Task updated successfully", status=True, status_code=200)


@app.route('/get/<string:type>', methods=['GET'])
def get(type):
    """
    Returns all the tasks based on the type
    """
    if type == 'all':
        tasks = Todo.query.all()
    elif type == 'complete':
        tasks = Todo.query.filter_by(is_complete=True).all()
    elif type == 'incomplete':
        tasks = Todo.query.filter_by(is_complete=False).all()
    
    data = [task.serialize() for task in tasks]
    return api_response(data, message="Tasks fetched successfully", status=True, status_code=200)