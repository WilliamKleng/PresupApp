import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Configuración de la base de datos para Railway
db_uri = os.environ.get('DATABASE_URL')

if db_uri:
    # Ajuste necesario para SQLAlchemy 1.4+ ya que Railway usa 'postgres://'
    if db_uri.startswith("postgres://"):
        db_uri = db_uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
else:
    # Fallback para desarrollo local
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///presupuestos.db'

# Configuración de seguridad y otros
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cambia-esto-por-un-secreto')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Importación de modelos y rutas
from app import models
from app import routes
from app import clientes_routes
from app import presupuestos_routes
from app import remitos_routes
from app import pdf_routes
from app import historial_routes

# Inicialización de la base de datos (se activa con la variable INIT_DB=true en Railway)
if os.environ.get('INIT_DB') == 'true':
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    app.run(debug=True)