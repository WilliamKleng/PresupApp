from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.models import Presupuesto, Cliente, PresupuestoItem
from datetime import date

def _save_items(presupuesto_id, conceptos, cantidades, precios):
    """Helper function to save or update items for a given budget."""
    PresupuestoItem.query.filter_by(presupuesto_id=presupuesto_id).delete()
    for i in range(len(conceptos)):
        if conceptos[i] and cantidades[i] and precios[i]:
            try:
                cantidad = float(cantidades[i])
                precio = float(precios[i])
                item = PresupuestoItem(
                    presupuesto_id=presupuesto_id,
                    orden=i + 1,
                    concepto=conceptos[i],
                    cantidad=cantidad,
                    precio_unitario=precio,
                    total=cantidad * precio
                )
                db.session.add(item)
            except (ValueError, TypeError):
                flash(f"Error en los datos del ítem '{conceptos[i]}'. Se omitió.", "error")

@app.route('/presupuestos')
def presupuestos():
    """Redirects to the new budget form, as the list view is deprecated."""
    return redirect(url_for('nuevo_presupuesto'))

@app.route('/presupuestos/nuevo', methods=['GET', 'POST'])
def nuevo_presupuesto():
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        if not cliente_id:
            flash('Debe seleccionar un cliente.', 'error')
            # Redirect back to the form with entered data if possible, or just the blank form
            return redirect(url_for('nuevo_presupuesto'))
        
        fecha_str = request.form.get('fecha')
        fecha = date.fromisoformat(fecha_str) if fecha_str else date.today()
        
        ultimo_numero = db.session.query(db.func.max(Presupuesto.numero)).scalar() or 0
        
        nuevo_presupuesto = Presupuesto(
            numero=ultimo_numero + 1,
            cliente_id=cliente_id,
            fecha=fecha,
            iva_porcentaje=float(request.form.get('iva_porcentaje')) if request.form.get('iva_porcentaje') else None,
            notas=request.form.get('notas')
        )
        db.session.add(nuevo_presupuesto)
        db.session.flush() # Use flush to get the ID for the items before committing

        _save_items(
            nuevo_presupuesto.id,
            request.form.getlist('concepto'),
            request.form.getlist('cantidad'),
            request.form.getlist('precio_unitario')
        )
        
        db.session.commit()
        flash('Presupuesto creado exitosamente.')
        return redirect(url_for('historial'))
    
    # GET request
    clientes = Cliente.query.order_by(Cliente.nombre).all()
    ultimo_numero = db.session.query(db.func.max(Presupuesto.numero)).scalar() or 0
    return render_template(
        'formulario_presupuesto.html', 
        presupuesto=None, 
        clientes=clientes, 
        next_numero=ultimo_numero + 1,
        date=date
    )

@app.route('/presupuestos/<int:id>/editar', methods=['GET', 'POST'])
def editar_presupuesto(id):
    presupuesto = Presupuesto.query.get_or_404(id)
    if request.method == 'POST':
        presupuesto.cliente_id = request.form['cliente_id']
        fecha_str = request.form.get('fecha')
        presupuesto.fecha = date.fromisoformat(fecha_str) if fecha_str else presupuesto.fecha
        presupuesto.iva_porcentaje = float(request.form.get('iva_porcentaje')) if request.form.get('iva_porcentaje') else None
        presupuesto.notas = request.form.get('notas')

        _save_items(
            presupuesto.id,
            request.form.getlist('concepto'),
            request.form.getlist('cantidad'),
            request.form.getlist('precio_unitario')
        )

        db.session.commit()
        flash('Presupuesto actualizado.')
        return redirect(url_for('historial'))

    # GET request
    clientes = Cliente.query.order_by(Cliente.nombre).all()
    return render_template(
        'formulario_presupuesto.html', 
        presupuesto=presupuesto, 
        clientes=clientes,
        date=date
    )

@app.route('/presupuestos/<int:id>/eliminar', methods=['POST'])
def eliminar_presupuesto(id):
    presupuesto = Presupuesto.query.get_or_404(id)
    PresupuestoItem.query.filter_by(presupuesto_id=id).delete()
    db.session.delete(presupuesto)
    db.session.commit()
    flash('Presupuesto eliminado.')
    return redirect(url_for('historial'))

