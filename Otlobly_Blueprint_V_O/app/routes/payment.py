from flask import Blueprint, app, app, request, redirect, session, flash
from app.models import db, Order, Payment

payment = Blueprint('payment', __name__)


# ---------- PAYMENT ----------
@payment.route('/payment/add', methods=['POST'])
def add_payment():
    if 'user_id' not in session:
        return redirect('/login')

    order = db.session.get(Order, int(request.form['order_id']))

    if not order or order.user_id != session['user_id']:
        return "Unauthorized"

    if order.payment:
        return redirect('/dashboard')

    total = order.product.price * order.quantity

    payment = Payment(
        order=order,
        method="card",
        amount=total
    )
    
    order.status = "paid"

    db.session.add(payment)
    db.session.commit()

    return redirect('/dashboard')


@payment.route('/payment/<int:id>/delete')
def delete_payment_user(id):
    if 'user_id' not in session:
        return redirect('/login')

    payment = db.session.get(Payment, id)

    if not payment:
        return redirect('/dashboard')

    if payment.order.user_id != session['user_id']:
        return "Unauthorized"

    order = payment.order
    if order:
        order.status = "created"

    db.session.delete(payment)
    db.session.commit()

    flash("💳 Payment deleted", "warning")

    return redirect('/dashboard')