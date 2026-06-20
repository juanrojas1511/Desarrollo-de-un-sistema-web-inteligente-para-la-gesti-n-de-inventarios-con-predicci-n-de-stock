from flask import Flask, render_template,request,redirect

import pyodbc
app = Flask(__name__)
def conectar():

    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=DESKTOP-K8HOHEK\\SQLEXPRESS;'
        'DATABASE=InventarioDB;'
        'Trusted_Connection=yes;'
    )
# Página principal
@app.route('/')
def inicio():
    return render_template('index.html')

# Lista de productos
@app.route('/productos')
def productos():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT *
    FROM Productos
    """)

    lista = cursor.fetchall()

    conexion.close()

    return render_template(
        'productos.html',
        productos=lista
    )

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():

    if request.method == 'POST':

        nombre = request.form['nombre']
        stock = request.form['stock']
        stock_minimo = request.form['stock_minimo']
        precio = request.form['precio']
        tipo = request.form['tipo']

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
        INSERT INTO Productos
        (
            Nombre,
            Stock,
            StockMinimo,
            Precio,
            Tipo
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            nombre,
            stock,
            stock_minimo,
            precio,
            tipo
        ))

        conexion.commit()
        conexion.close()

        return redirect('/productos')

    return render_template('agregar.html')

@app.route('/dashboard')
def dashboard():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM Productos")
    total_productos = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM Productos
        WHERE Stock <= StockMinimo
    """)
    stock_bajo = cursor.fetchone()[0]

    cursor.execute("""
        SELECT Id, Nombre, Stock
        FROM Productos
    """)
    productos = cursor.fetchall()

    alertas = []

    for producto in productos:
        producto_id = producto[0]
        nombre = producto[1]
        stock = producto[2]

        cursor.execute("""
            SELECT AVG(CAST(CantidadVendida AS FLOAT))
            FROM HistorialVentas
            WHERE ProductoId = ?
        """, (producto_id,))

        promedio = cursor.fetchone()[0]

        if promedio is not None and promedio > 0:
            dias = round(stock / promedio, 1)
        else:
            dias = "Sin historial"

        alertas.append({
            "nombre": nombre,
            "stock": stock,
            "dias": dias
        })

    conexion.close()

    return render_template(
        "dashboard.html",
        total_productos=total_productos,
        stock_bajo=stock_bajo,
        alertas=alertas
    )
@app.route('/vender/<int:id>', methods=['GET', 'POST'])
def vender(id):

     
    conexion = conectar()
    cursor = conexion.cursor()

    if request.method == 'POST':

        cantidad = int(request.form['cantidad'])

        # Guardar venta en historial
        cursor.execute("""
        INSERT INTO HistorialVentas
        (ProductoId, CantidadVendida)
        VALUES (?, ?)
        """, (id, cantidad))

        # Restar stock
        cursor.execute("""
        UPDATE Productos
        SET Stock = Stock - ?
        WHERE Id = ?
        """, (cantidad, id))

        conexion.commit()

        return redirect('/productos')

    # Obtener datos del producto
    cursor.execute("""
    SELECT *
    FROM Productos
    WHERE Id = ?
    """, (id,))

    producto = cursor.fetchone()

    conexion.close()

    return render_template(
        'vender.html',
        producto=producto
    )
@app.route('/movimiento', methods=['GET', 'POST'])
def movimiento():

    conexion = pyodbc.connect(
      'DRIVER={SQL Server};'
    'SERVER=DESKTOP-K8HOHEK\\SQLEXPRESS;'
    'DATABASE=InventarioDB;'
    'Trusted_Connection=yes;'
    )

    cursor = conexion.cursor()

    if request.method == 'POST':

        producto_id = request.form['producto_id']
        cantidad = int(request.form['cantidad'])
        tipo = request.form['tipo']

        cursor.execute("""
            INSERT INTO Movimientos
            (ProductoId, Cantidad, Tipo)
            VALUES (?, ?, ?)
        """,
        (producto_id, cantidad, tipo))

        if tipo == 'ENTRADA':

            cursor.execute("""
                UPDATE Productos
                SET Stock = Stock + ?
                WHERE Id = ?
            """,
            (cantidad, producto_id))

        else:

            cursor.execute("""
                UPDATE Productos
                SET Stock = Stock - ?
                WHERE Id = ?
            """,
            (cantidad, producto_id))

        conexion.commit()

        return redirect('/dashboard')

    cursor.execute("SELECT Id, Nombre FROM Productos")

    productos = cursor.fetchall()

    conexion.close()

    return render_template(
        'movimiento.html',
        productos=productos
    )



if __name__ == '__main__':
    app.run(debug=True)