from app import db
from flask_login import UserMixin
from datetime import datetime

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(50))
    mail = db.Column(db.String(120))
    dni_cuit = db.Column(db.String(30))  # DNI/CUIT del cliente
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    presupuestos = db.relationship('Presupuesto', back_populates='cliente', cascade="all, delete-orphan")
    remitos = db.relationship('Remito', back_populates='cliente', cascade="all, delete-orphan")

class Presupuesto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    iva_porcentaje = db.Column(db.Float)
    notas = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    cliente = db.relationship('Cliente', back_populates='presupuestos')
    items = db.relationship('PresupuestoItem', back_populates='presupuesto', cascade="all, delete-orphan")

class PresupuestoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    presupuesto_id = db.Column(db.Integer, db.ForeignKey('presupuesto.id'), nullable=False)
    orden = db.Column(db.Integer)
    concepto = db.Column(db.String(200), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    presupuesto = db.relationship('Presupuesto', back_populates='items')

class Remito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    notas = db.Column(db.Text)
    cliente = db.relationship('Cliente', back_populates='remitos')
    items = db.relationship('RemitoItem', back_populates='remito', cascade="all, delete-orphan", order_by='RemitoItem.orden')


class RemitoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    remito_id = db.Column(db.Integer, db.ForeignKey('remito.id'), nullable=False)
    orden = db.Column(db.Integer)
    descripcion = db.Column(db.String(250), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    remito = db.relationship('Remito', back_populates='items')
