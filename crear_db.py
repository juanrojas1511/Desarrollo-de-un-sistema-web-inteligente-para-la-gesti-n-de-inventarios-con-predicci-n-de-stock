import sqlite3

conexion = sqlite3.connect("database.db")
cursor = conexion.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

# Borrar tablas si ya existen
cursor.execute("DROP TABLE IF EXISTS HistorialVentas")
cursor.execute("DROP TABLE IF EXISTS Movimientos")
cursor.execute("DROP TABLE IF EXISTS Productos")

# Crear tabla Productos
cursor.execute("""
CREATE TABLE Productos(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT,
    Stock INTEGER,
    StockMinimo INTEGER,
    Precio REAL,
    Tipo TEXT,
    FechaRegistro DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Crear tabla Movimientos
cursor.execute("""
CREATE TABLE Movimientos(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductoId INTEGER,
    Cantidad INTEGER,
    Precio REAL,
    Tipo TEXT,
    Fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(ProductoId) REFERENCES Productos(Id)
)
""")

# Crear tabla HistorialVentas
cursor.execute("""
CREATE TABLE HistorialVentas(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductoId INTEGER,
    CantidadVendida INTEGER,
    Fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(ProductoId) REFERENCES Productos(Id)
)
""")

# Insertar productos
cursor.executemany("""
INSERT INTO Productos (Nombre, Stock, StockMinimo, Precio, Tipo)
VALUES (?, ?, ?, ?, ?)
""", [
    ('Laptop Lenovo', 80, 15, 2800.00, 'Electronico'),
    ('Mouse Gamer', 45, 10, 75.00, 'Accesorio'),
    ('Teclado Mecánico', 60, 12, 180.00, 'Accesorio'),
    ('Monitor Samsung', 35, 8, 650.00, 'Electronico'),
    ('Impresora Epson', 25, 5, 720.00, 'Oficina')
])

# Insertar historial de ventas
cursor.executemany("""
INSERT INTO HistorialVentas (ProductoId, CantidadVendida, Fecha)
VALUES (?, ?, ?)
""", [
    (1, 8, '2026-06-01'),
    (1, 10, '2026-06-02'),
    (1, 9, '2026-06-03'),
    (1, 11, '2026-06-04'),
    (1, 10, '2026-06-05'),

    (2, 6, '2026-06-01'),
    (2, 5, '2026-06-02'),
    (2, 7, '2026-06-03'),
    (2, 6, '2026-06-04'),
    (2, 8, '2026-06-05'),

    (3, 4, '2026-06-01'),
    (3, 6, '2026-06-02'),
    (3, 5, '2026-06-03'),
    (3, 4, '2026-06-04'),
    (3, 6, '2026-06-05'),

    (4, 3, '2026-06-01'),
    (4, 4, '2026-06-02'),
    (4, 3, '2026-06-03'),
    (4, 5, '2026-06-04'),
    (4, 4, '2026-06-05'),

    (5, 2, '2026-06-01'),
    (5, 3, '2026-06-02'),
    (5, 2, '2026-06-03'),
    (5, 4, '2026-06-04'),
    (5, 3, '2026-06-05')
])

conexion.commit()
conexion.close()

print("Base de datos database.db creada correctamente.")