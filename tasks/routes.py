from flask import Blueprint, request, jsonify, session
from models import db, Task, User, UserTask
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__, url_prefix="/api")

@tasks_bp.route("/check_session")
def check_session():
    user_id = session.get("user_id")
    if user_id:
        return jsonify({
            "user_id": user_id,
            "email": session.get("email"),
            "first_name": session.get("first_name")
        })
    return jsonify({}), 200

# GET all tasks
@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    current_user_id = session["user_id"]
    tasks = (
        db.session.query(Task)
        .join(UserTask)
        .filter(UserTask.user_id == current_user_id)
        .all()
        )
    
    return jsonify([task.to_dict() for task in tasks])

# POST create new task
@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    current_user_id = session["user_id"]
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
    db.session.flush()  # assign new_task.id without committing yet
    
    newLink = UserTask(user_id = current_user_id, task_id = new_task.id)
    db.session.add(newLink)
    db.session.commit()
    
    return jsonify(new_task.to_dict()), 201

# PUT update task
@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    task = Task.query.get_or_404(task_id)
    data = request.json
    
    
    current_user_id = session["user_id"]
    link = UserTask.query.filter_by(user_id=current_user_id, task_id=task_id).first()
    if not link:
        return jsonify({"error": "Unauthorized"}), 401
    
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
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    current_user_id = session["user_id"]

    # Find link 
    link = UserTask.query.filter_by(user_id=current_user_id, task_id=task_id).first()
    if not link:
        return jsonify({"error": "Task not found for this user"}), 404
    
    db.session.delete(link)
    
    
    # Check task belongs to other users
    other_links = UserTask.query.filter_by(task_id=task_id).all()
    if not other_links:
        # if wala, bye2
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        
        
    db.session.commit()
    return '', 204