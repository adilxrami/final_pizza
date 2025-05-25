from flask import Blueprint, request, redirect, url_for, session, Response, jsonify
from database import SessionLocal
from models import User
from utils import login_required
from helpers import get_html_and_css

auth = Blueprint('auth', __name__)

def encrypt(pw):
    return "".join(chr(ord(c) + 3) for c in pw)

def decrypt(pw):
    return "".join(chr(ord(c) - 3) for c in pw)

@auth.route("/", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "")
        email = request.form.get("email", "")
        phone = request.form.get("phone", "")
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not all([username, email, phone, password, confirm_password]):
            session['error'] = "All fields are required"
            return redirect(url_for("auth.signup"))

        if password != confirm_password:
            session['error'] = "Passwords do not match"
            return redirect(url_for("auth.signup"))

        if "@" not in email or "." not in email.split("@")[-1] or len(email.split("@")) != 2:
            session['error'] = "Invalid email format"
            return redirect(url_for("auth.signup"))

        if len(password) < 8:
            session['error'] = "Password must be at least 8 characters"
            return redirect(url_for("auth.signup"))

        session_db = SessionLocal()
        if session_db.query(User).filter_by(email=email).first():
            session['error'] = "Email is already registered"
            session_db.close()
            return redirect(url_for("auth.signup"))

        new_user = User(name=username, email=email, phone=phone, password=encrypt(password))
        session_db.add(new_user)
        session_db.commit()
        session_db.close()
        return redirect(url_for("auth.signin"))

    return Response(get_html_and_css("signup", "signup", data={"pagetitle": "Sign Up"}), mimetype="text/html")

@auth.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            session['error'] = "Email and password are required."
            return redirect(url_for("auth.signin"))

        session_db = SessionLocal()
        user = session_db.query(User).filter_by(email=email).first()
        session_db.close()

        if not user or decrypt(user.password) != password:
            session['error'] = "Incorrect email or password."
            return redirect(url_for("auth.signin"))

        session['email'] = user.email
        session['username'] = user.name
        return redirect(url_for('orders.usermenu'))

    return Response(get_html_and_css("signin", "signup", data={"pagetitle": "Sign In"}), mimetype="text/html")

@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('auth.signin', success="You have been logged out."))

@auth.route("/geteror")
def get_error():
    return {"error": session.pop('error', None)}

@auth.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    session_db = SessionLocal()
    user = session_db.query(User).filter_by(email=session['email']).first()

    if request.method == "POST":
        if decrypt(user.password) != request.form["oldpassword"]:
            session_db.close()
            return redirect(url_for("auth.edit_profile", error="Old password is incorrect."))

        if request.form["password"] != request.form["confirm_password"]:
            session_db.close()
            return redirect(url_for("auth.edit_profile", error="New passwords do not match."))

        user.name = request.form["username"]
        user.email = request.form["email"]
        user.phone = request.form["phone"]
        user.password = encrypt(request.form["password"])
        session_db.commit()
        session_db.close()
        
        return redirect(url_for("auth.profile_success"))
    session_db.close()
    return Response(get_html_and_css("edit_profile", "signup", data={
        "pagetitle": "Edit Profile",
        "error": request.args.get("error")
    }), mimetype="text/html")
@auth.route("/profile_success")
def profile_success():
    return Response(get_html_and_css("profile_success", "order_status", data={
        "pagetitle": "Profile Updated",
        "message": "Your profile has been updated successfully!"
    }), mimetype="text/html")
@auth.route("/api/user_info")
@login_required
def user_info():
    session_db = SessionLocal()
    user = session_db.query(User).filter_by(email=session.get("email")).first()
    session_db.close()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "username": user.name,
        "email": user.email,
        "phone": user.phone,
        "success": request.args.get("success")
    })
