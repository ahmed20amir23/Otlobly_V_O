from flask import Flask
from dotenv import load_dotenv
import os
from app.models import db

def create_app():
    load_dotenv('secret.env')

    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    db.init_app(app)
 
    from app.routes.auth import auth
    from app.routes.main import main
    from app.routes.orders import orders
    from app.routes.payment import payment
    from app.routes.admin import admin

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(orders)
    app.register_blueprint(payment)
    app.register_blueprint(admin)

    return app