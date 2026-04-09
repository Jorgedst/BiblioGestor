from database.conexion import get_connection


def execute_query(query, values=None):
    connection = get_connection()
    if connection is None:
        return False, "Error de conexión"
    try:
        cursor = connection.cursor()
        cursor.execute(query, values or ())
        connection.commit()
        return True, cursor
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        connection.close()
        
def fetch_query(query, values=None):
    connection = get_connection()
    if connection is None:
        return False, "Error de conexión"
    try:
        cursor = connection.cursor()
        cursor.execute(query, values or ())
        data = cursor.fetchall()
        return True, data
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        connection.close()

def validarUser(codigo, campo : str):
    query = f"SELECT * FROM usuarios WHERE {campo} = %s"
    success, data = fetch_query(query, (codigo,))
    if success:
        return len(data) > 0, data
    else:
        return False, data

def obtenerUsuarioInfo(id):
    query = "SELECT * FROM usuarios WHERE codigo = %s"
    success, data = fetch_query(query, (id,))
    if success and data:
        return data
    else:
        return None

def registrar_Usuario(codigoEstudiante, identificacion, nombre, apellido, correo, esEstudiante,estado, carrera):
    query = """insert into usuarios(codigo, identificación,nombre,apellido,correo,rol,estado,carrera)
	values( %s,%s,%s,%s,%s,%s,%s,%s
    )
    """
    success, result = execute_query(
        query, (codigoEstudiante, identificacion, nombre, apellido, correo, esEstudiante,estado, carrera))
    if success:
        return True, "Usuario Registrado"
    else:
        return False, result


def actualizarUsuario(codigo, nombre, apellido, correo, carrera):
    query = """UPDATE usuarios
               SET nombre = %s, apellido = %s, correo = %s, carrera = %s
               WHERE codigo = %s"""
    success, result = execute_query(query, (nombre, apellido, correo, carrera, codigo))
    if success:
        return True, "Usuario actualizado"
    else:
        return False, result


def eliminarUsuario(codigo):
    query = "DELETE FROM usuarios WHERE codigo = %s"
    success, result = execute_query(query, (codigo,))
    if success:
        return True, "Usuario eliminado"
    else:
        return False, result


def registrar_libro(isbn, titulo, autores, editorial, anio, categoria, descripcion):
    query = """INSERT INTO libros (isbn, titulo, autores, editorial, año, categoría, descripción)
               VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    success, result = execute_query(
        query, (isbn, titulo, autores, editorial, anio, categoria, descripcion)
    )
    if success:
        return True, "Libro registrado"
    else:
        return False, result


def registrar_ejemplar(id_ejemplar, codigo_isbn, ubicacion, estado):
    query = """INSERT INTO ejemplaresfisicos (idEjemplar, codigoIsbn, ubicación, estado)
               VALUES (%s, %s, %s, %s)"""
    success, result = execute_query(
        query, (id_ejemplar, codigo_isbn, ubicacion, estado)
    )
    if success:
        return True, "Ejemplar registrado"
    else:
        return False, result


# ── Validaciones de existencia (PK única) ────────────────────────

def existeISBN(isbn):
    """Retorna True si el ISBN ya existe en la tabla Libros."""
    query = "SELECT isbn FROM libros WHERE isbn = %s"
    success, data = fetch_query(query, (isbn,))
    if success:
        return len(data) > 0
    return False


def existeEjemplar(id_ejemplar):
    """Retorna True si el idEjemplar ya existe en ejemplaresfisicos."""
    query = "SELECT idEjemplar FROM ejemplaresfisicos WHERE idEjemplar = %s"
    success, data = fetch_query(query, (id_ejemplar,))
    if success:
        return len(data) > 0
    return False


# ── Listados ─────────────────────────────────────────────────────

def obtenerLibros():
    """Retorna todos los libros."""
    query = "SELECT * FROM libros"
    success, data = fetch_query(query)
    if success:
        return data
    return []


def obtenerEjemplaresPorISBN(isbn):
    """Retorna los ejemplares físicos asociados a un ISBN."""
    query = "SELECT * FROM ejemplaresfisicos WHERE codigoIsbn = %s"
    success, data = fetch_query(query, (isbn,))
    if success:
        return data
    return []


# ── Actualización ────────────────────────────────────────────────

def actualizarLibro(isbn, titulo, autores, editorial, anio, categoria, descripcion):
    query = """UPDATE libros
               SET titulo = %s, autores = %s, editorial = %s, año = %s,
                   categoría = %s, descripción = %s
               WHERE isbn = %s"""
    success, result = execute_query(
        query, (titulo, autores, editorial, anio, categoria, descripcion, isbn)
    )
    if success:
        return True, "Libro actualizado"
    else:
        return False, result


def actualizarEjemplar(id_ejemplar, ubicacion, estado):
    query = """UPDATE ejemplaresfisicos
               SET ubicación = %s, estado = %s
               WHERE idEjemplar = %s"""
    success, result = execute_query(query, (ubicacion, estado, id_ejemplar))
    if success:
        return True, "Ejemplar actualizado"
    else:
        return False, result


# ── Eliminación ──────────────────────────────────────────────────

def eliminarLibro(isbn):
    query = "DELETE FROM libros WHERE isbn = %s"
    success, result = execute_query(query, (isbn,))
    if success:
        return True, "Libro eliminado"
    else:
        return False, result


def eliminarEjemplar(id_ejemplar):
    query = "DELETE FROM ejemplaresfisicos WHERE idEjemplar = %s"
    success, result = execute_query(query, (id_ejemplar,))
    if success:
        return True, "Ejemplar eliminado"
    else:
        return False, result


# ── Inventario ───────────────────────────────────────────────────

def obtenerEjemplaresPorEstado(estado):
    """
    Retorna ejemplares filtrados por estado con info del libro.
    Columnas: idEjemplar, codigoIsbn, ubicación, estado, titulo, autores
    """
    query = """
        SELECT ef.idEjemplar, ef.codigoIsbn, ef.ubicación, ef.estado,
               l.titulo, l.autores
        FROM ejemplaresfisicos ef
        INNER JOIN libros l ON l.isbn = ef.codigoIsbn
        WHERE ef.estado = %s
        ORDER BY l.titulo, ef.idEjemplar
    """
    success, data = fetch_query(query, (estado,))
    if success:
        return data
    return []


# ── Dashboard usuario ────────────────────────────────────────────

def obtenerCategorias():
    """Retorna las categorías distintas de los libros (no nulas)."""
    query = "SELECT DISTINCT categoría FROM libros WHERE categoría IS NOT NULL AND categoría <> '' ORDER BY categoría"
    success, data = fetch_query(query)
    if success:
        return [row[0] for row in data]
    return []


def obtenerLibrosFiltrados(texto_busqueda: str = "", categoria: str = "", solo_disponibles: bool = False):
    """
    Retorna libros filtrados por texto (título/autores/ISBN),
    categoría y disponibilidad de ejemplares.
    """
    if solo_disponibles:
        query = """
            SELECT DISTINCT l.isbn, l.titulo, l.autores, l.editorial,
                            l.año, l.categoría, l.descripción
            FROM libros l
            INNER JOIN ejemplaresfisicos ef ON ef.codigoIsbn = l.isbn
            WHERE ef.estado = 'Disponible'
        """
    else:
        query = """
            SELECT l.isbn, l.titulo, l.autores, l.editorial,
                   l.año, l.categoría, l.descripción
            FROM libros l
            WHERE 1=1
        """

    values = []

    if texto_busqueda:
        query += " AND (l.titulo LIKE %s OR l.autores LIKE %s OR CAST(l.isbn AS CHAR) LIKE %s)"
        like = f"%{texto_busqueda}%"
        values.extend([like, like, like])

    if categoria:
        query += " AND l.categoría = %s"
        values.append(categoria)

    query += " ORDER BY l.titulo"

    success, data = fetch_query(query, tuple(values) if values else None)
    if success:
        return data
    return []


# ── Préstamos ────────────────────────────────────────────────────

def obtenerEjemplarDisponible(isbn):
    """Retorna el primer ejemplar con estado 'Disponible' para un ISBN, o None."""
    query = "SELECT idEjemplar FROM ejemplaresfisicos WHERE codigoIsbn = %s AND estado = 'Disponible' LIMIT 1"
    success, data = fetch_query(query, (isbn,))
    if success and data:
        return data[0][0]
    return None


def actualizarEstadoEjemplar(id_ejemplar, estado):
    """Cambia el estado de un ejemplar (Disponible / Prestado / Perdido)."""
    query = "UPDATE ejemplaresfisicos SET estado = %s WHERE idEjemplar = %s"
    success, result = execute_query(query, (estado, id_ejemplar))
    return success


def obtenerSiguienteIdPrestamo():
    """Retorna el siguiente ID disponible para un préstamo."""
    query = "SELECT MAX(idPrestamo) FROM prestamos"
    success, data = fetch_query(query)
    if success and data and data[0][0] is not None:
        return data[0][0] + 1
    return 1


def registrarPrestamo(id_prestamo, codigo_usuario, ejemplar, fecha_prestamo, fecha_vencimiento):
    """Registra un préstamo."""
    query = """INSERT INTO prestamos (idPrestamo, codigoUsuario, ejemplar, fechaPrestamo, fechaVencimiento)
               VALUES (%s, %s, %s, %s, %s)"""
    success, result = execute_query(
        query, (id_prestamo, codigo_usuario, ejemplar, fecha_prestamo, fecha_vencimiento)
    )
    if success:
        return True, "Préstamo registrado"
    else:
        return False, result


def obtenerPrestamosUsuario(codigo_usuario):
    """
    Retorna los préstamos activos de un usuario (sin devolución registrada).
    Columnas: idPrestamo, ejemplar, fechaPrestamo, fechaVencimiento, titulo, autores, descripción
    """
    query = """
        SELECT p.idPrestamo, p.ejemplar, p.fechaPrestamo, p.fechaVencimiento,
               l.titulo, l.autores, l.descripción
        FROM prestamos p
        INNER JOIN ejemplaresfisicos ef ON ef.idEjemplar = p.ejemplar
        INNER JOIN libros l ON l.isbn = ef.codigoIsbn
        WHERE p.codigoUsuario = %s
          AND NOT EXISTS (SELECT 1 FROM devoluciones d WHERE d.idPrestamo = p.idPrestamo)
        ORDER BY p.fechaPrestamo DESC
    """
    success, data = fetch_query(query, (codigo_usuario,))
    if success:
        return data
    return []


def obtenerHistorialPrestamosUsuario(codigo_usuario):
    """
    Retorna TODOS los préstamos de un usuario (activos + devueltos).
    Columnas: idPrestamo, ejemplar, fechaPrestamo, fechaVencimiento,
              titulo, autores, descripción, devuelto (1/0)
    """
    query = """
        SELECT p.idPrestamo, p.ejemplar, p.fechaPrestamo, p.fechaVencimiento,
               l.titulo, l.autores, l.descripción,
               CASE WHEN d.idDevolucion IS NOT NULL THEN 1 ELSE 0 END AS devuelto
        FROM prestamos p
        INNER JOIN ejemplaresfisicos ef ON ef.idEjemplar = p.ejemplar
        INNER JOIN libros l ON l.isbn = ef.codigoIsbn
        LEFT JOIN devoluciones d ON d.idPrestamo = p.idPrestamo
        WHERE p.codigoUsuario = %s
        ORDER BY p.fechaPrestamo DESC
    """
    success, data = fetch_query(query, (codigo_usuario,))
    if success:
        return data
    return []


# ── Gestión admin ────────────────────────────────────────────────

def obtenerPrestamosActivos():
    """
    Préstamos activos (sin devolución registrada).
    Columnas: idPrestamo, nombreUsuario, titulo, ejemplar, fechaPrestamo, fechaVencimiento
    """
    query = """
        SELECT p.idPrestamo,
               CONCAT(u.nombre, ' ', u.apellido) AS nombreUsuario,
               l.titulo, p.ejemplar,
               p.fechaPrestamo, p.fechaVencimiento
        FROM prestamos p
        INNER JOIN usuarios u ON u.codigo = p.codigoUsuario
        INNER JOIN ejemplaresfisicos ef ON ef.idEjemplar = p.ejemplar
        INNER JOIN libros l ON l.isbn = ef.codigoIsbn
        WHERE NOT EXISTS (SELECT 1 FROM devoluciones d WHERE d.idPrestamo = p.idPrestamo)
        ORDER BY p.fechaPrestamo DESC
    """
    success, data = fetch_query(query)
    if success:
        return data
    return []


def obtenerPrestamosVencidos():
    """
    Préstamos activos cuya fechaVencimiento ya pasó.
    Columnas: idPrestamo, nombreUsuario, titulo, ejemplar, fechaPrestamo, fechaVencimiento
    """
    query = """
        SELECT p.idPrestamo,
               CONCAT(u.nombre, ' ', u.apellido) AS nombreUsuario,
               l.titulo, p.ejemplar,
               p.fechaPrestamo, p.fechaVencimiento
        FROM prestamos p
        INNER JOIN usuarios u ON u.codigo = p.codigoUsuario
        INNER JOIN ejemplaresfisicos ef ON ef.idEjemplar = p.ejemplar
        INNER JOIN libros l ON l.isbn = ef.codigoIsbn
        WHERE NOT EXISTS (SELECT 1 FROM devoluciones d WHERE d.idPrestamo = p.idPrestamo)
          AND p.fechaVencimiento < NOW()
        ORDER BY p.fechaVencimiento ASC
    """
    success, data = fetch_query(query)
    if success:
        return data
    return []


def obtenerUsuariosMasPrestamos():
    """
    Top 10 usuarios con más préstamos.
    Columnas: codigoUsuario, nombreUsuario, totalPrestamos
    """
    query = """
        SELECT p.codigoUsuario,
               CONCAT(u.nombre, ' ', u.apellido) AS nombreUsuario,
               COUNT(*) AS totalPrestamos
        FROM prestamos p
        INNER JOIN usuarios u ON u.codigo = p.codigoUsuario
        GROUP BY p.codigoUsuario, u.nombre, u.apellido
        ORDER BY totalPrestamos DESC
        LIMIT 10
    """
    success, data = fetch_query(query)
    if success:
        return data
    return []


def obtenerLibrosMasPrestados(fecha_desde=None, fecha_hasta=None):
    """
    Top 10 libros más prestados, opcionalmente filtrados por rango de fechas.
    Columnas: isbn, titulo, autores, totalPrestamos
    """
    query = """
        SELECT l.isbn, l.titulo, l.autores, COUNT(*) AS totalPrestamos
        FROM prestamos p
        INNER JOIN ejemplaresfisicos ef ON ef.idEjemplar = p.ejemplar
        INNER JOIN libros l ON l.isbn = ef.codigoIsbn
        WHERE 1=1
    """
    values = []
    if fecha_desde:
        query += " AND p.fechaPrestamo >= %s"
        values.append(fecha_desde)
    if fecha_hasta:
        query += " AND p.fechaPrestamo <= %s"
        values.append(fecha_hasta)
    query += " GROUP BY l.isbn, l.titulo, l.autores ORDER BY totalPrestamos DESC LIMIT 10"
    success, data = fetch_query(query, tuple(values) if values else None)
    if success:
        return data
    return []


def obtenerPrestamosRecientes():
    """
    Retorna todos los préstamos con info de usuario y libro para el admin.
    Columnas: idPrestamo, codigoUsuario, nombreUsuario, ejemplar, titulo,
              fechaPrestamo, fechaVencimiento
    """
    query = """
        SELECT p.idPrestamo, p.codigoUsuario,
               CONCAT(u.nombre, ' ', u.apellido) AS nombreUsuario,
               p.ejemplar,
               l.titulo,
               p.fechaPrestamo, p.fechaVencimiento
        FROM prestamos p
        INNER JOIN usuarios u ON u.codigo = p.codigoUsuario
        INNER JOIN ejemplaresfisicos ef ON ef.idEjemplar = p.ejemplar
        INNER JOIN libros l ON l.isbn = ef.codigoIsbn
        ORDER BY p.fechaPrestamo DESC
    """
    success, data = fetch_query(query)
    if success:
        return data
    return []


def denegarPrestamo(id_prestamo):
    """
    Deniega un préstamo: elimina el registro y libera el ejemplar.
    """
    # Obtener el ejemplar para liberarlo
    query_ej = "SELECT ejemplar FROM prestamos WHERE idPrestamo = %s"
    success, data = fetch_query(query_ej, (id_prestamo,))
    if success and data:
        ejemplar_id = data[0][0]
        actualizarEstadoEjemplar(ejemplar_id, "Disponible")

    query = "DELETE FROM prestamos WHERE idPrestamo = %s"
    success, result = execute_query(query, (id_prestamo,))
    if success:
        return True, "Préstamo denegado"
    return False, result


# ── Devoluciones ─────────────────────────────────────────────────

def obtenerSiguienteIdDevolucion():
    """Retorna el siguiente ID disponible para una devolución."""
    query = "SELECT MAX(idDevolucion) FROM devoluciones"
    success, data = fetch_query(query)
    if success and data and data[0][0] is not None:
        return data[0][0] + 1
    return 1


def registrarDevolucion(id_devolucion, id_prestamo, observaciones=""):
    """Registra una devolución y libera el ejemplar."""
    # Obtener el ejemplar del préstamo para liberarlo
    query_ej = "SELECT ejemplar FROM prestamos WHERE idPrestamo = %s"
    success, data = fetch_query(query_ej, (id_prestamo,))
    if success and data:
        ejemplar_id = data[0][0]
        actualizarEstadoEjemplar(ejemplar_id, "Disponible")

    query = """INSERT INTO devoluciones (idDevolucion, idPrestamo, observaciones)
               VALUES (%s, %s, %s)"""
    success, result = execute_query(query, (id_devolucion, id_prestamo, observaciones))
    if success:
        return True, "Devolución registrada"
    return False, result


def obtenerDevoluciones():
    """
    Retorna todas las devoluciones con info del préstamo, usuario y libro.
    Columnas: idDevolucion, idPrestamo, observaciones, codigoUsuario, nombreUsuario,
              titulo, ejemplar
    """
    query = """
        SELECT d.idDevolucion, d.idPrestamo, d.observaciones,
               p.codigoUsuario,
               CONCAT(u.nombre, ' ', u.apellido) AS nombreUsuario,
               l.titulo, p.ejemplar
        FROM devoluciones d
        INNER JOIN prestamos p ON p.idPrestamo = d.idPrestamo
        INNER JOIN usuarios u ON u.codigo = p.codigoUsuario
        INNER JOIN ejemplaresfisicos ef ON ef.idEjemplar = p.ejemplar
        INNER JOIN libros l ON l.isbn = ef.codigoIsbn
        ORDER BY d.idDevolucion DESC
    """
    success, data = fetch_query(query)
    if success:
        return data
    return []


def yaExisteDevolucion(id_prestamo):
    """Comprueba si ya existe una devolución para un préstamo."""
    query = "SELECT idDevolucion FROM devoluciones WHERE idPrestamo = %s"
    success, data = fetch_query(query, (id_prestamo,))
    if success:
        return len(data) > 0
    return False

