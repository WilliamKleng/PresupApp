from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_login import LoginManager
import os

app = Flask(__name__)

# Railway expone la base en DATABASE_URL. En local se usa SQLite.
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cambia-esto-por-un-secreto')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///presupuestos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)
# login_manager = LoginManager(app)


from app import models
from app import routes
from app import clientes_routes
from app import presupuestos_routes
from app import remitos_routes
from app import pdf_routes
from app import historial_routes

# Rutas y vistas se agregarán aquí                                                                                                                                                                  

if os.environ.get('INIT_DB') == 'true':
    with app.app_context():
        db.create_all()
