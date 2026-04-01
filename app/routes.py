from flask import render_template
from app import app
from app.models import Presupuesto, Cliente, Remito
import datetime
import locale

# Set locale to Spanish for date formatting
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'es')
    except locale.Error:
        pass # Keep default locale if Spanish is not available

@app.route('/')
def index():
    n_presupuestos = Presupuesto.query.count()
    n_remitos = Remito.query.count()
    n_clientes = Cliente.query.count()

    recent_presupuestos = Presupuesto.query.order_by(Presupuesto.fecha.desc()).limit(5).all()
    recent_remitos = Remito.query.order_by(Remito.fecha.desc()).limit(5).all()
    
    current_date = datetime.date.today().strftime('%A, %d de %B de %Y')

    return render_template(
        'index.html', 
        n_presupuestos=n_presupuestos,
        n_remitos=n_remitos,
        n_clientes=n_clientes,
        recent_presupuestos=recent_presupuestos,
        recent_remitos=recent_remitos,
        current_date=current_date
    )
