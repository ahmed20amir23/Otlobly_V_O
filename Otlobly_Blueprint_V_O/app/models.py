from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ================= MODELS =================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20), default="user")

    orders = db.relationship(
        'Order',
        backref='user',
        cascade="all, delete-orphan"
    )


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)

    orders = db.relationship('Order', backref='product')


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, default=1)
    status = db.Column(db.String(50), default="created")

    payment = db.relationship(
        'Payment',
        backref='order',
        uselist=False,
        cascade="all, delete-orphan"
    )


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    method = db.Column(db.String(50))
    amount = db.Column(db.Float)
