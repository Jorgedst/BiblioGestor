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
    # 1. Recuperar ejemplares en préstamo activo para volver a ponerlos disponibles
    query_ejemplares = """
        SELECT p.ejemplar FROM prestamos p
        WHERE p.codigoUsuario = %s
          AND p.estadoPrestamo IN ('En solicitud', 'Aprobada')
          AND NOT EXISTS (
              SELECT 1 FROM devoluciones d 
              WHERE d.idPrestamo = p.idPrestamo AND d.estadoDevolucion = 'Aprobada'
          )
    """
    success_ej, ejemplares = fetch_query(query_ejemplares, (codigo,))
    if success_ej and ejemplares:
        for row in ejemplares:
            execute_query("UPDATE ejemplaresfisicos SET estado = 'Disponible' WHERE idEjemplar = %s", (row[0],))
            
    # 2. Borrar las devoluciones asociadas a los préstamos de este usuario
    query_del_dev = """
        DELETE FROM devoluciones 
        WHERE idPrestamo IN (
            SELECT idPrestamo FROM prestamos WHERE codigoUsuario = %s
        )
    """
    execute_query(query_del_dev, (codigo,))
    
    # 3. Borrar los préstamos
    execute_query("DELETE FROM prestamos WHERE codigoUsuario = %s", (codigo,))

    # 4. Finalmente, borrar al usuario
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
    Para el estado 'Prestado', solo se retornan los que tienen un préstamo activo aprobado.
    Columnas: idEjemplar, codigoIsbn, ubicación, estado, titulo, autores
    """
    if estado == 'Prestado':
        query = """
            SELECT DISTINCT ef.idEjemplar, ef.codigoIsbn, ef.ubicación, ef.estado,
                   l.titulo, l.autores
            FROM ejemplaresfisicos ef
            INNER JOIN libros l ON l.isbn = ef.codigoIsbn
            INNER JOIN prestamos p ON p.ejemplar = ef.idEjemplar
            WHERE ef.estado = 'Prestado'
              AND p.estadoPrestamo = 'Aprobada'
              AND NOT EXISTS (
                  SELECT 1 FROM devoluciones d WHERE d.idPrestamo = p.idPrestamo AND d.estadoDevolucion = 'Aprobada'
              )
            ORDER BY l.titulo, ef.idEjemplar
        """
        success, data = fetch_query(query)
    else:
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
    """Registra un préstamo con estado 'En solicitud'."""
    query = """INSERT INTO prestamos (idPrestamo, codigoUsuario, ejemplar, fechaPrestamo, fechaVencimiento, estadoPrestamo)
               VALUES (%s, %s, %s, %s, %s, 'En solicitud')"""
    success, result = execute_query(
        query, (id_prestamo, codigo_usuario, ejemplar, fecha_prestamo, fecha_vencimiento)
    )
    if success:
        return True, "Préstamo registrado"
    else:
        return False, result


def obtenerPrestamosUsuario(codigo_usuario):
    """
    Retorna los préstamos activos de un usuario (aprobados, sin devolución aprobada).
    Columnas: idPrestamo, ejemplar, fechaPrestamo, fechaVencimiento, titulo, autores, descripción
    """
    query = """
        SELECT p.idPrestamo, p.ejemplar, p.fechaPrestamo, p.fechaVencimiento,
               l.titulo, l.autores, l.descripción
        FROM prestamos p
        INNER JOIN ejemplaresfisicos ef ON ef.idEjemplar = p.ejemplar
        INNER JOIN libros l ON l.isbn = ef.codigoIsbn
        WHERE p.codigoUsuario = %s
          AND p.estadoPrestamo = 'Aprobada'
          AND NOT EXISTS (SELECT 1 FROM devoluciones d WHERE d.idPrestamo = p.idPrestamo AND d.estadoDevolucion = 'Aprobada')
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
              titulo, autores, descripción, devuelto (1/0), estadoPrestamo
    """
    query = """
        SELECT p.idPrestamo, p.ejemplar, p.fechaPrestamo, p.fechaVencimiento,
               l.titulo, l.autores, l.descripción,
               CASE WHEN d.idDevolucion IS NOT NULL AND d.estadoDevolucion = 'Aprobada' THEN 1 ELSE 0 END AS devuelto,
               p.estadoPrestamo
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
    Préstamos activos (aprobados, sin devolución aprobada).
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
        WHERE p.estadoPrestamo = 'Aprobada'
          AND NOT EXISTS (SELECT 1 FROM devoluciones d WHERE d.idPrestamo = p.idPrestamo AND d.estadoDevolucion = 'Aprobada')
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
        WHERE p.estadoPrestamo = 'Aprobada'
          AND NOT EXISTS (SELECT 1 FROM devoluciones d WHERE d.idPrestamo = p.idPrestamo AND d.estadoDevolucion = 'Aprobada')
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
              fechaPrestamo, fechaVencimiento, estadoPrestamo
    """
    query = """
        SELECT p.idPrestamo, p.codigoUsuario,
               CONCAT(u.nombre, ' ', u.apellido) AS nombreUsuario,
               p.ejemplar,
               l.titulo,
               p.fechaPrestamo, p.fechaVencimiento,
               p.estadoPrestamo
        FROM prestamos p
        INNER JOIN usuarios u ON u.codigo = p.codigoUsuario
        INNER JOIN ejemplaresfisicos ef ON ef.idEjemplar = p.ejemplar
        INNER JOIN libros l ON l.isbn = ef.codigoIsbn
        ORDER BY FIELD(p.estadoPrestamo, 'En solicitud', 'Aprobada', 'Rechazada'), p.fechaPrestamo DESC
    """
    success, data = fetch_query(query)
    if success:
        return data
    return []


def aprobarPrestamo(id_prestamo):
    """Aprueba un préstamo: cambia estado a 'Aprobada'."""
    query = "UPDATE prestamos SET estadoPrestamo = 'Aprobada' WHERE idPrestamo = %s"
    success, result = execute_query(query, (id_prestamo,))
    if success:
        return True, "Préstamo aprobado"
    return False, result


def rechazarPrestamo(id_prestamo):
    """
    Rechaza un préstamo: cambia estado a 'Rechazada' y libera el ejemplar.
    """
    query_ej = "SELECT ejemplar FROM prestamos WHERE idPrestamo = %s"
    success, data = fetch_query(query_ej, (id_prestamo,))
    if success and data:
        ejemplar_id = data[0][0]
        actualizarEstadoEjemplar(ejemplar_id, "Disponible")

    query = "UPDATE prestamos SET estadoPrestamo = 'Rechazada' WHERE idPrestamo = %s"
    success, result = execute_query(query, (id_prestamo,))
    if success:
        return True, "Préstamo rechazado"
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
    """Registra una solicitud de devolución (estado 'En solicitud'). NO libera el ejemplar."""
    import datetime
    fecha_dev = datetime.datetime.now()
    query = """INSERT INTO devoluciones (idDevolucion, idPrestamo, observaciones, estadoDevolucion, fechaDevolucion)
               VALUES (%s, %s, %s, 'En solicitud', %s)"""
    success, result = execute_query(query, (id_devolucion, id_prestamo, observaciones, fecha_dev))
    if success:
        return True, "Solicitud de devolución registrada"
    return False, result


def aprobarDevolucion(id_devolucion, observaciones, tarifa):
    """Aprueba una devolución: guarda observación + tarifa y libera el ejemplar."""
    # Obtener el ejemplar del préstamo para liberarlo
    query_ej = """
        SELECT p.ejemplar FROM devoluciones d
        INNER JOIN prestamos p ON p.idPrestamo = d.idPrestamo
        WHERE d.idDevolucion = %s
    """
    success, data = fetch_query(query_ej, (id_devolucion,))
    if success and data:
        ejemplar_id = data[0][0]
        actualizarEstadoEjemplar(ejemplar_id, "Disponible")

    query = """UPDATE devoluciones
               SET estadoDevolucion = 'Aprobada', observaciones = %s, tarifaCobro = %s
               WHERE idDevolucion = %s"""
    success, result = execute_query(query, (observaciones, tarifa, id_devolucion))
    if success:
        return True, "Devolución aprobada"
    return False, result


def rechazarDevolucion(id_devolucion, observaciones):
    """Rechaza una devolución con observación."""
    query = """UPDATE devoluciones
               SET estadoDevolucion = 'Rechazada', observaciones = %s
               WHERE idDevolucion = %s"""
    success, result = execute_query(query, (observaciones, id_devolucion))
    if success:
        return True, "Devolución rechazada"
    return False, result


def calcularTarifaTardia(fecha_prestamo):
    """Calcula la tarifa por entrega tardía ($10,000/día después de 15 días)."""
    import datetime
    if not fecha_prestamo:
        return 0
    if isinstance(fecha_prestamo, str):
        fecha_prestamo = datetime.datetime.strptime(fecha_prestamo, "%Y-%m-%d %H:%M:%S")
    dias = (datetime.datetime.now() - fecha_prestamo).days
    if dias > 15:
        return (dias - 15) * 10000
    return 0


def obtenerDevoluciones():
    """
    Retorna todas las devoluciones con info del préstamo, usuario y libro.
    Columnas: idDevolucion, idPrestamo, observaciones, codigoUsuario, nombreUsuario,
              titulo, ejemplar, estadoDevolucion, tarifaCobro, fechaDevolucion, fechaPrestamo
    """
    query = """
        SELECT d.idDevolucion, d.idPrestamo, d.observaciones,
               p.codigoUsuario,
               CONCAT(u.nombre, ' ', u.apellido) AS nombreUsuario,
               l.titulo, p.ejemplar,
               d.estadoDevolucion, d.tarifaCobro, d.fechaDevolucion,
               p.fechaPrestamo
        FROM devoluciones d
        INNER JOIN prestamos p ON p.idPrestamo = d.idPrestamo
        INNER JOIN usuarios u ON u.codigo = p.codigoUsuario
        INNER JOIN ejemplaresfisicos ef ON ef.idEjemplar = p.ejemplar
        INNER JOIN libros l ON l.isbn = ef.codigoIsbn
        ORDER BY FIELD(d.estadoDevolucion, 'En solicitud', 'Aprobada', 'Rechazada'), d.idDevolucion DESC
    """
    success, data = fetch_query(query)
    if success:
        return data
    return []


def yaExisteDevolucion(id_prestamo):
    """Comprueba si ya existe una devolución pendiente o aprobada para un préstamo."""
    query = "SELECT idDevolucion FROM devoluciones WHERE idPrestamo = %s AND estadoDevolucion IN ('En solicitud', 'Aprobada')"
    success, data = fetch_query(query, (id_prestamo,))
    if success:
        return len(data) > 0
    return False

