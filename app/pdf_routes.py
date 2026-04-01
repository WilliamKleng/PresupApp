from flask import render_template, make_response, request
from app import app
from app.models import Presupuesto, PresupuestoItem, Remito
import weasyprint

@app.route('/presupuestos/<int:id>/pdf')
def presupuesto_pdf(id):
    presupuesto = Presupuesto.query.get_or_404(id)
    items = PresupuestoItem.query.filter_by(presupuesto_id=id).all()
    # Recalcula desde cantidad x precio para evitar inconsistencias en datos viejos.
    subtotal = sum((item.cantidad or 0) * (item.precio_unitario or 0) for item in items)
    iva_porcentaje = presupuesto.iva_porcentaje or 0
    iva_monto = subtotal * (iva_porcentaje / 100) if iva_porcentaje else 0
    total = subtotal + iva_monto

    rendered = render_template(
        'presupuesto_pdf.html',
        presupuesto=presupuesto,
        items=items,
        subtotal=subtotal,
        iva_monto=iva_monto,
        total=total,
    )
    pdf = weasyprint.HTML(string=rendered).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    filename = f'presupuesto_{presupuesto.numero:04d}.pdf'
    disposition = 'attachment' if request.args.get('download') == '1' else 'inline'
    response.headers['Content-Disposition'] = f'{disposition}; filename={filename}'
    return response

@app.route('/remitos/<int:id>/pdf')
def remito_pdf(id):
    remito = Remito.query.get_or_404(id)
    rendered = render_template('remito_pdf.html', remito=remito)
    pdf = weasyprint.HTML(string=rendered).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    filename = f'remito_{remito.numero:04d}.pdf'
    disposition = 'attachment' if request.args.get('download') == '1' else 'inline'
    response.headers['Content-Disposition'] = f'{disposition}; filename={filename}'
    return response
