from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.models import Cliente

@app.route('/clientes')
def clientes():
    lista = Cliente.query.order_by(Cliente.nombre).all()
    return render_template('clientes.html', clientes=lista)

@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        mail = request.form['mail']
        dni_cuit = request.form.get('dni_cuit')
        if not nombre:
            flash('El nombre es obligatorio.')
            return redirect(url_for('nuevo_cliente'))
        cliente = Cliente(nombre=nombre, direccion=direccion, telefono=telefono, mail=mail, dni_cuit=dni_cuit)
        db.session.add(cliente)
        db.session.commit()
        flash('Cliente creado exitosamente.')
        return redirect(url_for('clientes'))
    return render_template('nuevo_cliente.html')


@app.route('/clientes/<int:id>/editar', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    if request.method == 'POST':
        cliente.nombre = request.form['nombre']
        cliente.direccion = request.form['direccion']
        cliente.telefono = request.form['telefono']
        cliente.mail = request.form['mail']
        cliente.dni_cuit = request.form.get('dni_cuit')
        db.session.commit()
        flash('Cliente actualizado.')
        return redirect(url_for('clientes'))
    return render_template('editar_cliente.html', cliente=cliente)

@app.route('/clientes/<int:id>/eliminar', methods=['POST'])
def eliminar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente eliminado.')
    return redirect(url_for('clientes'))
