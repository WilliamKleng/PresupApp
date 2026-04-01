from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_login import LoginManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cambia-esto-por-un-secreto'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///presupuestos.db'
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

if __name__ == '__main__':
    app.run(debug=True)
