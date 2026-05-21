from flask import Blueprint, app, app, render_template, request, redirect, flash, session
from functools import wraps
from app.models import db, User, Product, Order, Payment

admin = Blueprint('admin', __name__)

# ================= ADMIN DECORATOR =================
def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')

        user = db.session.get(User, session['user_id'])

        if not user or user.role != "admin":
            return "Unauthorized", 403

        return f(*args, **kwargs)
    return wrapper
    
# ================= ADMIN =================
@admin.route('/admin')
@admin_required
def admin_dashboard():
    users = User.query.all()
    orders = Order.query.all()
    payments = Payment.query.all()

    return render_template("admin.html", users=users, orders=orders, payments=payments)

@admin.route('/admin/product/add', methods=['POST'])
@admin_required
def add_product():
    name = request.form['name']
    price = float(request.form['price'])

    product = Product(
        name=name,
        price=price
    )
    if Product.query.filter_by(name=name).first():
        flash("Product already exists", "warning")
        return redirect('/admin')

    db.session.add(product)
    db.session.commit()

    flash("✅ Product added successfully", "success")

    return redirect('/admin')


@admin.route('/admin/user/<int:id>/delete')
@admin_required
def delete_user(id):
    user = db.session.get(User, id)

    if not user:
        return redirect('/admin')

    if user.role == "admin":
        flash("Cannot delete admin", "danger")
        return redirect('/admin')

    if user.id == session['user_id']:
        flash("You cannot delete yourself", "danger")
        return redirect('/admin')

    db.session.delete(user)
    db.session.commit()

    return redirect('/admin')

@admin.route('/admin/payment/<int:id>/delete')
@admin_required
def delete_payment_admin(id):
    payment = db.session.get(Payment, id)

    if not payment:
        return redirect('/admin')

    order = payment.order
    if order:
        order.status = "created"

    db.session.delete(payment)
    db.session.commit()

    flash("💳 Payment deleted", "warning")

    return redirect('/admin')
