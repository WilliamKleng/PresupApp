from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.models import Remito, Cliente, RemitoItem
from datetime import date

@app.route('/remitos')
def remitos():
    """Redirects to the new remito form, as the list view is deprecated."""
    return redirect(url_for('nuevo_remito'))

@app.route('/remitos/nuevo', methods=['GET', 'POST'])
def nuevo_remito():
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        if not cliente_id:
            flash('Debe seleccionar un cliente.', 'error')
            return redirect(url_for('nuevo_remito'))

        fecha_str = request.form.get('fecha')
        fecha = date.fromisoformat(fecha_str) if fecha_str else date.today()
        
        ultimo_numero = db.session.query(db.func.max(Remito.numero)).scalar() or 0

        descripciones = request.form.getlist('descripcion')
        cantidades = request.form.getlist('cantidad')
        items_payload = []
        for idx, desc in enumerate(descripciones):
            descripcion = (desc or '').strip()
            if not descripcion:
                continue
            try:
                cantidad = float(cantidades[idx]) if idx < len(cantidades) else 1.0
            except (TypeError, ValueError):
                cantidad = 1.0
            if cantidad <= 0:
                cantidad = 1.0
            items_payload.append({'orden': idx + 1, 'descripcion': descripcion, 'cantidad': cantidad})

        if not items_payload and not (request.form.get('notas') or '').strip():
            flash('Debe cargar al menos un item o una nota de detalle.', 'error')
            return redirect(url_for('nuevo_remito'))
        
        nuevo_remito = Remito(
            numero=ultimo_numero + 1,
            cliente_id=cliente_id,
            fecha=fecha,
            notas=request.form.get('notas')
        )
        db.session.add(nuevo_remito)
        db.session.flush()

        for item in items_payload:
            db.session.add(
                RemitoItem(
                    remito_id=nuevo_remito.id,
                    orden=item['orden'],
                    descripcion=item['descripcion'],
                    cantidad=item['cantidad'],
                )
            )

        db.session.commit()
        flash('Remito creado exitosamente.')
        return redirect(url_for('historial'))

    # GET request
    clientes = Cliente.query.order_by(Cliente.nombre).all()
    ultimo_numero = db.session.query(db.func.max(Remito.numero)).scalar() or 0
    return render_template(
        'formulario_remito.html', 
        remito=None, 
        clientes=clientes, 
        next_numero=ultimo_numero + 1,
        date=date
    )

@app.route('/remitos/<int:id>/editar', methods=['GET', 'POST'])
def editar_remito(id):
    remito = Remito.query.get_or_404(id)
    if request.method == 'POST':
        remito.cliente_id = request.form['cliente_id']
        fecha_str = request.form.get('fecha')
        remito.fecha = date.fromisoformat(fecha_str) if fecha_str else remito.fecha
        remito.notas = request.form.get('notas')

        descripciones = request.form.getlist('descripcion')
        cantidades = request.form.getlist('cantidad')
        items_payload = []
        for idx, desc in enumerate(descripciones):
            descripcion = (desc or '').strip()
            if not descripcion:
                continue
            try:
                cantidad = float(cantidades[idx]) if idx < len(cantidades) else 1.0
            except (TypeError, ValueError):
                cantidad = 1.0
            if cantidad <= 0:
                cantidad = 1.0
            items_payload.append({'orden': idx + 1, 'descripcion': descripcion, 'cantidad': cantidad})

        if not items_payload and not (remito.notas or '').strip():
            flash('Debe cargar al menos un item o una nota de detalle.', 'error')
            return redirect(url_for('editar_remito', id=id))

        remito.items.clear()
        for item in items_payload:
            remito.items.append(
                RemitoItem(
                    orden=item['orden'],
                    descripcion=item['descripcion'],
                    cantidad=item['cantidad'],
                )
            )
        
        db.session.commit()
        flash('Remito actualizado.')
        return redirect(url_for('historial'))

    # GET request
    clientes = Cliente.query.order_by(Cliente.nombre).all()
    return render_template('formulario_remito.html', remito=remito, clientes=clientes, date=date)

@app.route('/remitos/<int:id>/eliminar', methods=['POST'])
def eliminar_remito(id):
    remito = Remito.query.get_or_404(id)
    db.session.delete(remito)
    db.session.commit()
    flash('Remito eliminado.')
    return redirect(url_for('historial'))
