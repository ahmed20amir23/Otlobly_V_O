from app import create_app
from app.models import db, User, Product
from werkzeug.security import generate_password_hash

app = create_app()

# with app.app_context():
#     db.create_all()

if __name__ == "__main__":
    app.run(debug=True)