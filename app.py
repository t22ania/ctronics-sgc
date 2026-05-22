# ============================================================
# C-TRONICS SOLUCIONES · Backend Flask + SQLite
# Sistema de Gestión Comercial
# ============================================================
# Modelo de datos basado en el diagrama de clases:
#   Usuario, Cliente, Categoria, Producto, Inventario,
#   Venta, DetalleVenta, Reporte
# ============================================================

from flask import Flask, jsonify, request, send_from_directory
import sqlite3
import os
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ctronics.db')


# ============================================================
# CONEXIÓN A LA BASE DE DATOS
# ============================================================
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


# ============================================================
# CREACIÓN DEL SCHEMA · 8 TABLAS SEGÚN DIAGRAMA DE CLASES
# ============================================================
def init_db():
    new_db = not os.path.exists(DB_PATH)
    conn = get_db()
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS Usuario (
        idUsuario       INTEGER PRIMARY KEY AUTOINCREMENT,
        nombreUsuario   TEXT NOT NULL UNIQUE,
        contrasena      TEXT NOT NULL,
        rol             TEXT NOT NULL DEFAULT 'Administrador',
        activo          INTEGER DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS Cliente (
        idCliente       INTEGER PRIMARY KEY AUTOINCREMENT,
        dniRuc          TEXT NOT NULL UNIQUE,
        nombres         TEXT NOT NULL,
        apellidos       TEXT DEFAULT '',
        telefono        TEXT DEFAULT '',
        email           TEXT DEFAULT '',
        direccion       TEXT DEFAULT '',
        totalComprado   REAL DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS Categoria (
        idCategoria     INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre          TEXT NOT NULL UNIQUE,
        descripcion     TEXT DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS Producto (
        idProducto      INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo          TEXT NOT NULL UNIQUE,
        nombre          TEXT NOT NULL,
        idCategoria     INTEGER,
        precioCosto     REAL NOT NULL DEFAULT 0,
        precioVenta     REAL NOT NULL DEFAULT 0,
        stock           INTEGER DEFAULT 0,
        stockMinimo     INTEGER DEFAULT 5,
        FOREIGN KEY (idCategoria) REFERENCES Categoria(idCategoria)
    );

    CREATE TABLE IF NOT EXISTS Inventario (
        idMovimiento    INTEGER PRIMARY KEY AUTOINCREMENT,
        idProducto      INTEGER NOT NULL,
        fecha           TEXT NOT NULL,
        tipoMovimiento  TEXT NOT NULL,
        cantidad        INTEGER NOT NULL,
        motivo          TEXT DEFAULT '',
        FOREIGN KEY (idProducto) REFERENCES Producto(idProducto)
    );

    CREATE TABLE IF NOT EXISTS Venta (
        idVenta         INTEGER PRIMARY KEY AUTOINCREMENT,
        idUsuario       INTEGER,
        idCliente       INTEGER NOT NULL,
        fecha           TEXT NOT NULL,
        subtotal        REAL NOT NULL,
        igv             REAL NOT NULL,
        total           REAL NOT NULL,
        estado          TEXT DEFAULT 'COMPLETADA',
        FOREIGN KEY (idUsuario) REFERENCES Usuario(idUsuario),
        FOREIGN KEY (idCliente) REFERENCES Cliente(idCliente)
    );

    CREATE TABLE IF NOT EXISTS DetalleVenta (
        idDetalle       INTEGER PRIMARY KEY AUTOINCREMENT,
        idVenta         INTEGER NOT NULL,
        idProducto      INTEGER NOT NULL,
        cantidad        INTEGER NOT NULL,
        precioUnitario  REAL NOT NULL,
        subtotal        REAL NOT NULL,
        FOREIGN KEY (idVenta) REFERENCES Venta(idVenta) ON DELETE CASCADE,
        FOREIGN KEY (idProducto) REFERENCES Producto(idProducto)
    );

    CREATE TABLE IF NOT EXISTS Reporte (
        idReporte         INTEGER PRIMARY KEY AUTOINCREMENT,
        idUsuario         INTEGER,
        tipo              TEXT NOT NULL,
        fechaInicio       TEXT,
        fechaFin          TEXT,
        fechaGeneracion   TEXT NOT NULL,
        FOREIGN KEY (idUsuario) REFERENCES Usuario(idUsuario)
    );
    """)

    if new_db:
        seed_data(cur)

    conn.commit()
    conn.close()


# ============================================================
# DATOS SEED (carga inicial)
# ============================================================
def seed_data(cur):
    # --- Usuario ---
    cur.execute(
        "INSERT INTO Usuario (nombreUsuario, contrasena, rol) VALUES (?,?,?)",
        ('admin', 'admin123', 'Administrador')
    )

    # --- Categorías ---
    cats = [
        ('SMARTPHONES', 'Telefonía celular'),
        ('ACCESORIOS',  'Cables, cargadores y periféricos menores'),
        ('CÓMPUTO',     'Equipos y periféricos de cómputo'),
        ('AUDIO',       'Parlantes, audífonos y micrófonos'),
        ('VIDEO',       'Televisores y monitores'),
    ]
    cur.executemany("INSERT INTO Categoria (nombre, descripcion) VALUES (?,?)", cats)

    cat_map = {r['nombre']: r['idCategoria']
               for r in cur.execute("SELECT idCategoria, nombre FROM Categoria").fetchall()}

    # --- Productos ---
    prods = [
        ('E-001', 'Samsung Galaxy A15',         'SMARTPHONES', 480,  689,  24, 5),
        ('E-002', 'Audífonos Bluetooth JBL',    'ACCESORIOS',  60,   120,  45, 10),
        ('E-003', 'Teclado Mecánico RGB',       'CÓMPUTO',     95,   180,  5,  8),
        ('E-004', 'Cargador 65W USB-C',         'ACCESORIOS',  35,   89,   2,  10),
        ('E-005', 'Mouse Inalámbrico Logitech', 'CÓMPUTO',     50,   95,   18, 6),
        ('E-006', 'iPhone 13 128GB',            'SMARTPHONES', 2200, 2899, 8,  3),
        ('E-007', 'Parlante JBL Go 3',          'AUDIO',       120,  199,  12, 5),
        ('E-008', 'Cable USB-C 1m',             'ACCESORIOS',  8,    20,   60, 15),
        ('E-009', 'Smart TV 43" 4K',            'VIDEO',       1100, 1499, 6,  2),
        ('E-010', 'Power Bank 20000mAh',        'ACCESORIOS',  55,   120,  14, 5),
    ]
    for cod, nom, cat, costo, precio, stock, smin in prods:
        cur.execute(
            """INSERT INTO Producto
               (codigo, nombre, idCategoria, precioCosto, precioVenta, stock, stockMinimo)
               VALUES (?,?,?,?,?,?,?)""",
            (cod, nom, cat_map[cat], costo, precio, stock, smin)
        )

    # --- Clientes ---
    cls = [
        ('45678912',    'María',                'Quispe Huamán',  '987654321', 'maria.q@gmail.com',     'Av. Brasil 123',         1245.50),
        ('12345678',    'José',                 'García Vargas',  '956123456', 'jose.garcia@hotmail.com','Jr. Cusco 456',         580.00),
        ('20512345678', 'Tienda El Sol SAC',    '',               '014567890', 'ventas@elsol.com.pe',   'Av. Wilson 789',         8450.00),
        ('78945612',    'Carlos',               'Mendoza Ríos',   '998877665', 'cmendoza@gmail.com',    'Calle Las Flores 321',   320.00),
        ('56789123',    'Ana Lucía',            'Torres',         '987112233', 'ana.torres@yahoo.es',   'Av. Arequipa 1500',      1899.00),
        ('20587634521', 'Distribuidora LR EIRL','',               '016654321', 'compras@lr.pe',         'Av. Argentina 200',      5230.00),
        ('42315678',    'Pedro',                'Salazar Aliaga', '945678901', 'pedrosalazar@gmail.com','Jr. Junín 88',           189.00),
        ('67891234',    'Rosa',                 'Fernández Cruz', '923456789', 'rosaf@outlook.com',     'Av. La Marina 999',      760.50),
    ]
    cur.executemany(
        """INSERT INTO Cliente
           (dniRuc, nombres, apellidos, telefono, email, direccion, totalComprado)
           VALUES (?,?,?,?,?,?,?)""",
        cls
    )

    # --- Ventas + DetalleVenta + movimientos de Inventario ---
    prod_id_map = {r['codigo']: r['idProducto']
                   for r in cur.execute("SELECT codigo, idProducto FROM Producto").fetchall()}
    today = datetime.now().strftime('%Y-%m-%d')

    ventas_data = [
        # (idCliente, hora, [(codigo_producto, cantidad, precio_unitario)])
        (1, '09:14', [('E-002', 1, 120)]),
        (2, '10:32', [('E-001', 1, 689)]),
        (4, '11:48', [('E-004', 2, 89), ('E-008', 1, 20)]),
        (5, '13:05', [('E-003', 1, 180), ('E-005', 1, 95)]),
        (7, '14:22', [('E-007', 1, 199)]),
    ]

    for cli_id, hora, items in ventas_data:
        total = sum(c * p for _, c, p in items)
        igv = total * 0.18 / 1.18
        base = total - igv
        fecha = f'{today} {hora}'

        cur.execute(
            """INSERT INTO Venta
               (idUsuario, idCliente, fecha, subtotal, igv, total, estado)
               VALUES (?,?,?,?,?,?,?)""",
            (1, cli_id, fecha, base, igv, total, 'COMPLETADA')
        )
        venta_id = cur.lastrowid

        for cod, cant, precio in items:
            pid = prod_id_map[cod]
            cur.execute(
                """INSERT INTO DetalleVenta
                   (idVenta, idProducto, cantidad, precioUnitario, subtotal)
                   VALUES (?,?,?,?,?)""",
                (venta_id, pid, cant, precio, cant * precio)
            )
            cur.execute(
                """INSERT INTO Inventario
                   (idProducto, fecha, tipoMovimiento, cantidad, motivo)
                   VALUES (?,?,?,?,?)""",
                (pid, fecha, 'SALIDA', cant, f'Venta #{venta_id}')
            )


# ============================================================
# RUTAS · Frontend
# ============================================================
@app.route('/')
def index():
    return send_from_directory('.', 'c-tronics.html')


# ============================================================
# API · CATEGORÍAS
# ============================================================
@app.route('/api/categorias')
def api_categorias():
    conn = get_db()
    rows = conn.execute("SELECT * FROM Categoria ORDER BY nombre").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


# ============================================================
# API · PRODUCTOS
# ============================================================
@app.route('/api/productos')
def api_productos():
    conn = get_db()
    rows = conn.execute("""
        SELECT p.*, c.nombre AS categoria
        FROM Producto p
        LEFT JOIN Categoria c ON p.idCategoria = c.idCategoria
        ORDER BY p.codigo
    """).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/productos', methods=['POST'])
def api_crear_producto():
    data = request.json
    conn = get_db()
    cat_row = conn.execute(
        "SELECT idCategoria FROM Categoria WHERE nombre=?", (data['categoria'],)
    ).fetchone()
    cat_id = cat_row['idCategoria'] if cat_row else None

    try:
        cur = conn.execute("""
            INSERT INTO Producto
            (codigo, nombre, idCategoria, precioCosto, precioVenta, stock, stockMinimo)
            VALUES (?,?,?,?,?,?,?)
        """, (data['codigo'], data['nombre'], cat_id, data['precioCosto'],
              data['precioVenta'], data['stock'], data['stockMinimo']))
        new_id = cur.lastrowid
        conn.commit()
        return jsonify({'ok': True, 'idProducto': new_id})
    except sqlite3.IntegrityError as e:
        return jsonify({'ok': False, 'error': f'Código duplicado: {data["codigo"]}'}), 400
    finally:
        conn.close()


@app.route('/api/productos/<int:pid>', methods=['PUT'])
def api_actualizar_producto(pid):
    data = request.json
    conn = get_db()
    cat_row = conn.execute(
        "SELECT idCategoria FROM Categoria WHERE nombre=?", (data['categoria'],)
    ).fetchone()
    cat_id = cat_row['idCategoria'] if cat_row else None

    conn.execute("""
        UPDATE Producto
        SET codigo=?, nombre=?, idCategoria=?, precioCosto=?, precioVenta=?, stock=?, stockMinimo=?
        WHERE idProducto=?
    """, (data['codigo'], data['nombre'], cat_id, data['precioCosto'],
          data['precioVenta'], data['stock'], data['stockMinimo'], pid))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})


@app.route('/api/productos/<int:pid>', methods=['DELETE'])
def api_eliminar_producto(pid):
    conn = get_db()
    conn.execute("DELETE FROM Producto WHERE idProducto=?", (pid,))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})


# ============================================================
# API · INVENTARIO
# ============================================================
@app.route('/api/inventario')
def api_inventario():
    """Movimientos recientes de inventario"""
    conn = get_db()
    rows = conn.execute("""
        SELECT i.*, p.codigo AS codigoProducto, p.nombre AS nombreProducto
        FROM Inventario i
        JOIN Producto p ON i.idProducto = p.idProducto
        ORDER BY i.fecha DESC
        LIMIT 100
    """).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/inventario/entrada', methods=['POST'])
def api_entrada_inventario():
    data = request.json
    conn = get_db()
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn.execute("""
        INSERT INTO Inventario
        (idProducto, fecha, tipoMovimiento, cantidad, motivo)
        VALUES (?,?,?,?,?)
    """, (data['idProducto'], fecha, 'ENTRADA',
          data['cantidad'], data.get('motivo', 'Reposición de stock')))

    conn.execute(
        "UPDATE Producto SET stock = stock + ? WHERE idProducto=?",
        (data['cantidad'], data['idProducto'])
    )
    conn.commit()
    conn.close()
    return jsonify({'ok': True})


# ============================================================
# API · CLIENTES
# ============================================================
@app.route('/api/clientes')
def api_clientes():
    conn = get_db()
    rows = conn.execute("SELECT * FROM Cliente ORDER BY nombres").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/clientes', methods=['POST'])
def api_crear_cliente():
    data = request.json
    conn = get_db()
    try:
        cur = conn.execute("""
            INSERT INTO Cliente
            (dniRuc, nombres, apellidos, telefono, email, direccion)
            VALUES (?,?,?,?,?,?)
        """, (data['dniRuc'], data['nombres'], data.get('apellidos', ''),
              data.get('telefono', ''), data.get('email', ''), data.get('direccion', '')))
        new_id = cur.lastrowid
        conn.commit()
        return jsonify({'ok': True, 'idCliente': new_id})
    except sqlite3.IntegrityError:
        return jsonify({'ok': False, 'error': 'DNI/RUC ya registrado'}), 400
    finally:
        conn.close()


@app.route('/api/clientes/<int:cid>', methods=['PUT'])
def api_actualizar_cliente(cid):
    data = request.json
    conn = get_db()
    conn.execute("""
        UPDATE Cliente
        SET dniRuc=?, nombres=?, apellidos=?, telefono=?, email=?, direccion=?
        WHERE idCliente=?
    """, (data['dniRuc'], data['nombres'], data.get('apellidos', ''),
          data.get('telefono', ''), data.get('email', ''),
          data.get('direccion', ''), cid))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})


@app.route('/api/clientes/<int:cid>', methods=['DELETE'])
def api_eliminar_cliente(cid):
    conn = get_db()
    conn.execute("DELETE FROM Cliente WHERE idCliente=?", (cid,))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})


@app.route('/api/clientes/<int:cid>/historial')
def api_historial_cliente(cid):
    conn = get_db()
    ventas = conn.execute("""
        SELECT v.*
        FROM Venta v
        WHERE v.idCliente = ?
        ORDER BY v.fecha DESC
    """, (cid,)).fetchall()

    result = []
    for v in ventas:
        d = dict(v)
        items = conn.execute("""
            SELECT d.*, p.nombre AS productoNombre
            FROM DetalleVenta d
            JOIN Producto p ON d.idProducto = p.idProducto
            WHERE d.idVenta = ?
        """, (v['idVenta'],)).fetchall()
        d['items'] = [dict(x) for x in items]
        result.append(d)
    conn.close()
    return jsonify(result)


# ============================================================
# API · VENTAS
# ============================================================
@app.route('/api/ventas')
def api_ventas():
    conn = get_db()
    ventas = conn.execute("""
        SELECT v.*,
               TRIM(c.nombres || ' ' || COALESCE(c.apellidos,'')) AS clienteNombre
        FROM Venta v
        JOIN Cliente c ON v.idCliente = c.idCliente
        ORDER BY v.fecha DESC
    """).fetchall()

    result = []
    for v in ventas:
        d = dict(v)
        items = conn.execute("""
            SELECT d.idDetalle, d.idProducto, d.cantidad, d.precioUnitario, d.subtotal,
                   p.nombre AS productoNombre
            FROM DetalleVenta d
            JOIN Producto p ON d.idProducto = p.idProducto
            WHERE d.idVenta = ?
        """, (v['idVenta'],)).fetchall()
        d['items'] = [dict(x) for x in items]
        result.append(d)
    conn.close()
    return jsonify(result)


@app.route('/api/ventas', methods=['POST'])
def api_crear_venta():
    data = request.json
    conn = get_db()
    items = data['items']

    # Validar stock antes de procesar
    for it in items:
        row = conn.execute(
            "SELECT stock, nombre FROM Producto WHERE idProducto=?",
            (it['prodId'],)
        ).fetchone()
        if not row or row['stock'] < it['cant']:
            conn.close()
            return jsonify({
                'ok': False,
                'error': f'Stock insuficiente para {row["nombre"] if row else "producto"}'
            }), 400

    # Totales
    total = sum(i['cant'] * i['precio'] for i in items)
    igv = total * 0.18 / 1.18
    base = total - igv
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M')

    # Cabecera de venta
    cur = conn.execute("""
        INSERT INTO Venta
        (idUsuario, idCliente, fecha, subtotal, igv, total, estado)
        VALUES (?,?,?,?,?,?,?)
    """, (1, data['idCliente'], fecha, base, igv, total, 'COMPLETADA'))
    venta_id = cur.lastrowid

    # Detalles + descuento de stock + movimientos de inventario
    for it in items:
        conn.execute("""
            INSERT INTO DetalleVenta
            (idVenta, idProducto, cantidad, precioUnitario, subtotal)
            VALUES (?,?,?,?,?)
        """, (venta_id, it['prodId'], it['cant'], it['precio'], it['cant'] * it['precio']))

        conn.execute(
            "UPDATE Producto SET stock = stock - ? WHERE idProducto=?",
            (it['cant'], it['prodId'])
        )
        conn.execute("""
            INSERT INTO Inventario
            (idProducto, fecha, tipoMovimiento, cantidad, motivo)
            VALUES (?,?,?,?,?)
        """, (it['prodId'], fecha, 'SALIDA', it['cant'], f'Venta #{venta_id}'))

    # Total comprado del cliente
    conn.execute(
        "UPDATE Cliente SET totalComprado = totalComprado + ? WHERE idCliente=?",
        (total, data['idCliente'])
    )

    conn.commit()
    conn.close()
    return jsonify({'ok': True, 'idVenta': venta_id, 'total': total})


# ============================================================
# API · DASHBOARD
# ============================================================
@app.route('/api/dashboard')
def api_dashboard():
    conn = get_db()
    total_prods = conn.execute("SELECT COUNT(*) c FROM Producto").fetchone()['c']
    stock_critico = conn.execute(
        "SELECT COUNT(*) c FROM Producto WHERE stock <= stockMinimo"
    ).fetchone()['c']
    total_clientes = conn.execute("SELECT COUNT(*) c FROM Cliente").fetchone()['c']

    today = datetime.now().strftime('%Y-%m-%d')
    ventas_hoy = conn.execute(
        "SELECT COALESCE(SUM(total),0) s, COUNT(*) c FROM Venta WHERE fecha LIKE ?",
        (f'{today}%',)
    ).fetchone()

    conn.close()
    return jsonify({
        'totalProductos': total_prods,
        'stockCritico': stock_critico,
        'totalClientes': total_clientes,
        'ventasHoyTotal': ventas_hoy['s'],
        'ventasHoyCount': ventas_hoy['c']
    })


# ============================================================
# API · REPORTES
# ============================================================
@app.route('/api/reportes/resumen')
def api_reporte_resumen():
    conn = get_db()
    ingresos = conn.execute("SELECT COALESCE(SUM(total),0) s FROM Venta").fetchone()['s']
    margen_total = conn.execute("""
        SELECT COALESCE(SUM((d.precioUnitario - p.precioCosto) * d.cantidad),0) m
        FROM DetalleVenta d
        JOIN Producto p ON d.idProducto = p.idProducto
    """).fetchone()['m']
    ventas_count = conn.execute("SELECT COUNT(*) c FROM Venta").fetchone()['c']

    top_prods = conn.execute("""
        SELECT p.nombre, SUM(d.cantidad) AS total
        FROM DetalleVenta d
        JOIN Producto p ON d.idProducto = p.idProducto
        GROUP BY p.idProducto
        ORDER BY total DESC
        LIMIT 5
    """).fetchall()

    conn.close()
    return jsonify({
        'ingresos': ingresos,
        'margen': margen_total,
        'margenPct': round(margen_total / ingresos * 100, 1) if ingresos else 0,
        'ventasCount': ventas_count,
        'topProductos': [dict(r) for r in top_prods]
    })


# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    init_db()
    print('=' * 64)
    print('  C-TRONICS SOLUCIONES · Sistema de Gestión Comercial')
    print('=' * 64)
    print(f'  Base de datos:  {DB_PATH}')
    print(f'  URL del sistema: http://localhost:5000')
    print(f'  Credenciales:   admin / admin123')
    print('=' * 64)
    print('  Presiona CTRL+C para detener el servidor')
    print('=' * 64)
    app.run(debug=False, port=5000, host='127.0.0.1')
