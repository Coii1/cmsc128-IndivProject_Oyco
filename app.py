from flask import Flask
from flask_cors import CORS
from auth.routes import auth_bp
from tasks.routes import tasks_bp
from models import db

app = Flask(__name__)
app.secret_key = "supersecretkey123"  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Change to your DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)  # Enable CORS for frontend communication

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(tasks_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database created!")
    app.run(debug=True, port=5000)