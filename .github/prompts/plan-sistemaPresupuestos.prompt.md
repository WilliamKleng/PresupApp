SISTEMA DE PRESUPUESTOS Y REMITOS — PLAN DE DESARROLLO
=========================================================

DESCRIPCIÓN DE LA APLICACIÓN
------------------------------
Aplicación web de uso personal para la gestión de presupuestos y
remitos de servicios/trabajos. Reemplaza el flujo manual en Excel
por un sistema centralizado accesible desde el navegador.

El sistema permite:
  - Gestionar una cartera de clientes (alta, edición, eliminación)
  - Crear presupuestos detallados con ítems de texto libre,
    cantidades, precios unitarios y opcionalmente IVA
  - Crear remitos vinculados a clientes con ítems sin precio
  - Numeración autoincremental y formateada (0001, 0002...) para
    presupuestos y remitos de forma independiente
  - Visualizar cada documento con un formato fiel al template
    original en Excel, listo para imprimir o exportar a PDF
  - Acceder a un panel resumen con los últimos movimientos

El acceso está protegido por login de usuario único (uso personal).
No requiere internet ni servidor externo: corre localmente.



STACK
-----
Backend:       Flask + Flask-Login
Base de datos: SQLite via SQLAlchemy
Frontend:      Jinja2 + CSS propio (design system del kiosk)
PDF/Impresión: WeasyPrint (genera PDF server-side)


BASE DE DATOS — ESQUEMA
------------------------

clientes
  id | nombre | direccion | telefono | mail | created_at

presupuestos
  id | numero (autoincremental) | cliente_id | fecha |
     iva_porcentaje (nullable) | notas | created_at

presupuesto_items
  id | presupuesto_id | orden | concepto | cantidad |
     precio_unitario | total

remitos
  id | numero (autoincremental) | cliente_id | fecha | notas
