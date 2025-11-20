from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint('auth', __name__)   

@auth_bp.route("/")
def index():
    return render_template("index.html")


@auth_bp.route("/accounts", methods=["POST"])
def create_account():
    data = request.get_json()
    
    # if User.query.filter_by(username=data['username']).first():
    #     return jsonify({'error': 'Username already exists'}), 400

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



@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        
        # cehck if ga exist
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"message": "Email not found"}), 404

        # if password is correct
        if not check_password_hash(user.password, password):
            return jsonify({"message": f"Incorrect password, The password is {user.password}"}), 401

        # store data in session 
        session["user_id"] = user.id
        session["email"] = user.email
        session["first_name"] = user.first_name
        
        print(user.first_name, "logged in")
        #ang downside gali sini kay if may error sa return me like indi ma serialize abi, na set nya na before ang sessio so pag nag refresh ka ga gwa na sya
        return jsonify({"message": f"Welcome back, {user.first_name}!", "username": f'{user.first_name}'}), 200
    except Exception as e:
        print("Login error:", e)
        return jsonify({"message": "Internal server error"}), 500
        
    

   
@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()  # removes all session data
    print("Session after logout:", dict(session))
    
    # Create a proper response object
    response = make_response(jsonify({"message": "Logged out successfully"}))
    response.status_code = 200
    
    # Clear cookies
    response.set_cookie("session", "", expires=0)
    response.set_cookie("csrf_token", "", expires=0)
    return response