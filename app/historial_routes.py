from flask import render_template, request
from app import app
from app.models import Cliente, Presupuesto, Remito

@app.route('/historial')
def historial():
    cliente_id = request.args.get('cliente_id', type=int)
    tipo = request.args.get('tipo', 'todos')
    clientes = Cliente.query.order_by(Cliente.nombre).all()
    presupuestos = []
    remitos = []
    if tipo in ('todos', 'presupuestos'):
        q = Presupuesto.query
        if cliente_id:
            q = q.filter_by(cliente_id=cliente_id)
        presupuestos = q.order_by(Presupuesto.fecha.desc()).all()
    if tipo in ('todos', 'remitos'):
        q = Remito.query
        if cliente_id:
            q = q.filter_by(cliente_id=cliente_id)
        remitos = q.order_by(Remito.fecha.desc()).all()
    return render_template('historial.html', clientes=clientes, presupuestos=presupuestos, remitos=remitos, cliente_id=cliente_id, tipo=tipo)
