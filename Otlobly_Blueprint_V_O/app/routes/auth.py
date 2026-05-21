from flask import Blueprint, app, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User
auth = Blueprint('auth', __name__)


# ---------- AUTH ----------
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(
            name=request.form['name'],
            email=request.form['email'],
            password=generate_password_hash(request.form['password'])
        )
        db.session.add(user)
        db.session.commit()
        return redirect('/login')

    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if not user:
            flash("Register First!!")
            return redirect('/register')
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            if user.role == "admin":
                return redirect('/admin')
            else:
                return redirect('/dashboard')
        else:
            flash("Invalid email or password")

    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

