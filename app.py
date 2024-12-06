from flask import Flask
from extensions import db, bcrypt, login_manager
from admin import setup_admin
from routes import routes_bp

celery_app = None

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./project.db"
app.config["SECRET_KEY"] = "your_secret_key_here"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["API_BASE_URL"] = "http://localhost:5001"


db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from model import Users
    return Users.query.get(user_id)


setup_admin(app, db)

app.register_blueprint(routes_bp)


if __name__ == "__main__":

    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
