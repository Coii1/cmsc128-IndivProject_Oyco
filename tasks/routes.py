from flask import Blueprint, request, jsonify, render_template
from models import db, Task
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__, url_prefix="/api")

# GET all tasks
@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.order_by(Task.date_created.desc()).all()
    return jsonify([task.to_dict() for task in tasks])

# POST create new task
@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    
    new_task = Task(
        name=data.get('name', 'Untitled Task'),
        completed=data.get('completed', False)
    )
    
    # Handle optional date
    if data.get('date'):
        try:
            new_task.dueDate = datetime.fromisoformat(data['date']).date()
        except ValueError:
            pass
    
    # Handle optional time
    if data.get('time'):
        try:
            new_task.due_time = datetime.strptime(data['time'], '%H:%M').time()
        except ValueError:
            pass
    
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify(new_task.to_dict()), 201

# PUT update task
@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.json
    
    if 'name' in data:
        task.name = data['name']
    if 'completed' in data:
        task.completed = data['completed']
    
    # Update date
    if 'date' in data:
        if data['date']:
            try:
                task.dueDate = datetime.fromisoformat(data['date']).date()
            except ValueError:
                task.dueDate = None
        else:
            task.dueDate = None
    
    # Update time
    if 'time' in data:
        if data['time']:
            try:
                task.due_time = datetime.strptime(data['time'], '%H:%M').time()
            except ValueError:
                task.due_time = None
        else:
            task.due_time = None
    
    db.session.commit()
    return jsonify(task.to_dict())

# DELETE task
@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204