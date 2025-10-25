from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    

@app.route("/")
def index():
    return render_template("login.html")


@app.route("/accounts", methods=["POST"])
def create_account():
    data = request.get_json()

    # Hash password before saving
    hashed_password = generate_password_hash(data.get("password"))

    new_user = User(
        first_name=data.get("firstName"),
        last_name=data.get("lastName"),
        email=data.get("email"),
        password=hashed_password
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully!"})
    except Exception as e:
        print("Error:", e)
        db.session.rollback()
        return jsonify({"message": "Error creating user."}), 500



@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    # cehck if ga exist
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Email not found"}), 404

    # if password is correct
    if not check_password_hash(user.password, password):
        return jsonify({"message": "Incorrect password"}), 401

    return jsonify({"message": f"Welcome back, {user.first_name}!"}), 200
    
@app.route("/logged")
def logged():
    return render_template("logged.html")

if __name__ == "__main__":

    with app.app_context():
        db.create_all()
        print("Database and tables created!")
    app.run(debug=True, port=5000)
    
    