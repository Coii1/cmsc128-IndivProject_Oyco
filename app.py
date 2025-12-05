from flask import Flask
from flask_cors import CORS
from auth.routes import auth_bp
from tasks.routes import tasks_bp
from models import db
import os  

app = Flask(__name__)

# Cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
is_production = os.getenv("FLASK_ENV") == "production" or os.getenv("PYTHONANYWHERE") == "true"
app.config['SESSION_COOKIE_SECURE'] = bool(is_production)

# Secret key (env in production)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

# Database: store app.db in Flask instance folder
os.makedirs(app.instance_path, exist_ok=True)
db_path = os.path.join(app.instance_path, 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# CORS:
origins_env = os.getenv("ALLOWED_ORIGINS", "")
origins = [o.strip() for o in origins_env.split(",") if o.strip()] if origins_env else None
if origins:
    CORS(app, supports_credentials=True, origins=origins)
else:
    CORS(app, supports_credentials=True)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(tasks_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database created!")
    app.run(debug=True, port=5000)