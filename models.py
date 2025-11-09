from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


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