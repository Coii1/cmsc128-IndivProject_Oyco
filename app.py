from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  # Change to your DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)  # Enable CORS for frontend communication

# Your Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    dueDate = db.Column(db.Date)
    due_time = db.Column(db.Time)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "completed": self.completed,
            "createdDate": self.date_created.strftime("%b %d"),
            "date": self.dueDate.isoformat() if self.dueDate else "",
            "time": self.due_time.strftime("%H:%M") if self.due_time else ""
        }

# Create tables
with app.app_context():
    db.create_all()
    
@app.route("/")
def index():
    return render_template("index.html")

# GET all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.order_by(Task.date_created.desc()).all()
    return jsonify([task.to_dict() for task in tasks])

# POST create new task
@app.route('/api/tasks', methods=['POST'])
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
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
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
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5000)