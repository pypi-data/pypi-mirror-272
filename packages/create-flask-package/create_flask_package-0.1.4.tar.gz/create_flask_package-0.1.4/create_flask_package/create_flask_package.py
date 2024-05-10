import os

def create_package(package_name):
    # Create package directory
    package_dir = os.path.join(package_name)
    os.makedirs(package_dir)

    # Create subdirectories and files
    os.makedirs(os.path.join(package_dir, 'static'))
    os.makedirs(os.path.join(package_dir, 'templates'))
    os.makedirs(os.path.join(package_dir, 'routes'))
    open(os.path.join(package_dir, '__init__.py'), 'a').close()
    open(os.path.join(package_dir, 'routes', 'test.py'), 'a').close()
    open(os.path.join(package_dir, 'db_queries.py'), 'a').close()
    open(os.path.join(package_dir, 'models.py'), 'a').close()
    open(os.path.join(package_dir, 'utils.py'), 'a').close()

    init_content = f"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from flask_cors import CORS
import os

db = SQLAlchemy()
app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config["SECRET_KEY"] = 'your key'
app.config["SESSION_TYPE"] = "sqlalchemy"
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config['SESSION_SQLALCHEMY'] = db
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 43200
Session(app)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///mydb.db'
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
from .routes.test import test_api as test_bp
app.register_blueprint(test_bp)
    """

    with open(f"{package_name}/__init__.py", "w") as f:
        f.write(init_content)
        
    models_content = """
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from . import db

# Sample model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
        """

    with open(f"{package_name}/models.py", "w") as f:
        f.write(models_content)
    
    routes_content = """
from flask import Blueprint

test_api = Blueprint('test_api', __name__)

@test_api.route('/')
def index():
    return "Hello, World!"
    """

    with open(f"{package_name}/routes/test.py", "w") as f:
        f.write(routes_content)
    
    # Create application.py at the same level as the package directory
    with open('application.py', 'w') as f:
        f.write(f'''from {package_name} import create_app

application, db = create_app()

if __name__ == "__main__":
    application.run(debug=True, host="0.0.0.0")
    ''')

    # Create setup.py
    setup_content = f"""
from setuptools import setup, find_packages

setup(
    name='create_flask_package',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-CORS',
        'Flask-Login',
        'Flask-Session'
    ]
)
"""

    with open('setup.py', 'w') as f:
        f.write(setup_content)

def create_package_entry_point():
    package_name = input("Enter the name of your package: ")
    create_package(package_name)

if __name__ == "__main__":
    create_package_entry_point()
