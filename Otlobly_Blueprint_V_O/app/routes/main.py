from flask import Blueprint, render_template, session, redirect
from app.models import db, User, Order, Product, Payment

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # db.create_all()
    # db.session.commit()
    return render_template('index.html')


# ---------- DASHBOARD ----------
@main.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    user = db.session.get(User, session['user_id'])

    if user.role == "admin":
        return redirect('/admin')

    orders = db.session.query(Order, Product)\
        .join(Product)\
        .filter(Order.user_id == user.id).all()

    payments = Payment.query.join(Order)\
        .filter(Order.user_id == user.id).all()

    total = sum([p.amount for p in payments])

    products = Product.query.all()

    return render_template(
        'dashboard.html',
        user=user,
        orders=orders,
        payments=payments,
        total=total,
        products=products
    )