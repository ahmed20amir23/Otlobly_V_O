from flask import Blueprint, app, flash, flash, request, redirect, session
from app.models import db, Order, Product, Payment

orders = Blueprint('orders', __name__)


# ---------- ORDERS ----------
@orders.route('/order', methods=['POST'])
def create_order():
    if 'user_id' not in session:
        return redirect('/login')

    product = db.session.get(Product, int(request.form['product_id']))
    quantity = int(request.form['quantity'])

    order = Order(
        user_id=session['user_id'],
        product_id=product.id,
        quantity=quantity,
        status="created"
    )

    db.session.add(order)
    db.session.commit()

    return redirect('/dashboard')


@orders.route('/order/<int:id>/update', methods=['POST'])
def update_order(id):
    if 'user_id' not in session:
        return redirect('/login')

    order = db.session.get(Order, id)

    if not order or order.user_id != session['user_id']:
        return "Unauthorized"

    order.product_id = request.form['product_id']
    order.quantity = int(request.form['quantity'])

    db.session.commit()

    return redirect('/dashboard')


@orders.route('/order/<int:id>/delete')
def delete_order(id):
    if 'user_id' not in session:
        return redirect('/login')

    order = db.session.get(Order, id)

    if not order or order.user_id != session['user_id']:
        return "Unauthorized"

    payment = Payment.query.filter_by(order_id=id).first()

    if payment:
        flash("Cannot delete a paid order", "warning")
        return redirect('/dashboard')

    db.session.delete(order)
    db.session.commit()

    return redirect('/dashboard')