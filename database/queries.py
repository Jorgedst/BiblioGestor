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


def aprobarDevolucionAutomatica(id_devolucion, observaciones):
    """Aprueba la devolución calculando internamente la multa y liberando el ejemplar."""
    # 1. Obtener el idPrestamo asociado a esta devolución
    query_prestamo = "SELECT idPrestamo FROM devoluciones WHERE idDevolucion = %s"
    success_p, p_data = fetch_query(query_prestamo, (id_devolucion,))
    
    if not success_p or not p_data:
        return False, "No se encontró el préstamo asociado a la devolución."
        
    id_prestamo = p_data[0][0]
    
    # 2. Calcular la multa real basada en los días de retraso
    tarifa_calculada = calcularTarifaTardiaDinámica(id_prestamo)

    # 3. Obtener y liberar el ejemplar físico
    query_ej = """
        SELECT p.ejemplar FROM devoluciones d
        INNER JOIN prestamos p ON p.idPrestamo = d.idPrestamo
        WHERE d.idDevolucion = %s
    """
    success_ej, data_ej = fetch_query(query_ej, (id_devolucion,))
    if success_ej and data_ej:
        ejemplar_id = data_ej[0][0]
        actualizarEstadoEjemplar(ejemplar_id, "Disponible")
        completarReserva(ejemplar_id)  # Si alguien lo tenía reservado, procesa la cola

    # 4. Actualizar la tabla de devoluciones
    query_update = """UPDATE devoluciones
                      SET estadoDevolucion = 'Aprobada', observaciones = %s, tarifaCobro = %s
                      WHERE idDevolucion = %s"""
    success, result = execute_query(query_update, (observaciones, tarifa_calculada, id_devolucion))
    
    if success:
        return True, f"Devolución aprobada con éxito. Multa total: ${tarifa_calculada:,}"
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


def calcularTarifaTardiaDinámica(id_prestamo):
    """Calcula la tarifa por entrega tardía ($10.000/día) basada en la fechaVencimiento real."""
    import datetime
    query = "SELECT fechaVencimiento FROM prestamos WHERE idPrestamo = %s"
    success, data = fetch_query(query, (id_prestamo,))
    
    if success and data and data[0][0]:
        fecha_vencimiento = data[0][0]
        if isinstance(fecha_vencimiento, str):
            fecha_vencimiento = datetime.datetime.strptime(fecha_vencimiento, "%Y-%m-%d %H:%M:%S")
            
        ahora = datetime.datetime.now()
        if ahora > fecha_vencimiento:
            dias_retraso = (ahora - fecha_vencimiento).days
            return dias_retraso * 10000
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


# ── Nuevas funciones para Reservas, Ampliaciones y Notificaciones ──

def obtenerEjemplaresNoDisponibles(isbn):
    """Obtiene los ejemplares no disponibles para un ISBN."""
    query = "SELECT idEjemplar FROM ejemplaresfisicos WHERE codigoIsbn = %s AND estado != 'Disponible'"
    success, data = fetch_query(query, (isbn,))
    if success:
        return data
    return []


def registrarReserva(codigo_usuario, id_ejemplar):
    """
    Registra una reserva activa de un ejemplar para un usuario.
    
    Validaciones:
    1. Verifica que el usuario exista y esté activo.
    2. Consulta el estado del ejemplar. Si es 'Disponible', no reserva.
    3. Verifica que no tenga reserva activa para este mismo ejemplar.
    """
    import datetime
    
    # ── 1. Validar que el usuario exista y esté activo ───────────
    ok_u, usuario = fetch_query(
        "SELECT codigo, estado FROM usuarios WHERE codigo = %s",
        (codigo_usuario,)
    )
    if not ok_u or not usuario:
        return False, f"No se encontró el usuario con código '{codigo_usuario}'."
    if usuario[0][1] != 1:
        return False, "El usuario no está activo en el sistema."

    # ── 2. Validar que el ejemplar exista ────────────────────────
    ok_e, ejemplar = fetch_query(
        "SELECT idEjemplar, estado FROM ejemplaresfisicos WHERE idEjemplar = %s",
        (id_ejemplar,)
    )
    if not ok_e or not ejemplar:
        return False, f"No se encontró el ejemplar con ID '{id_ejemplar}'."

    estado_ejemplar = ejemplar[0][1]

    # ── 3. Si está Disponible: no se reserva, se presta directo ──
    if estado_ejemplar == "Disponible":
        return False, (
            f"El ejemplar '{id_ejemplar}' está DISPONIBLE en este momento. "
            "No es necesario hacer una reserva; solicite el préstamo directamente."
        )

    # ── 4. Verificar que no exista ya una reserva activa igual ───
    ok_r, reserva_existente = fetch_query(
        "SELECT idReserva FROM reservas "
        "WHERE codigoUsuario = %s AND idEjemplar = %s AND estadoReserva = 'Activa'",
        (codigo_usuario, id_ejemplar)
    )
    if ok_r and reserva_existente:
        return False, "Ya existe una reserva activa para este usuario y ejemplar."

    # ── 5. Registrar la reserva ──────────────────────────────────
    ahora = datetime.datetime.now()
    query = "INSERT INTO reservas (codigoUsuario, idEjemplar, fechaReserva, estadoReserva) VALUES (%s, %s, %s, 'Activa')"
    success, result = execute_query(query, (codigo_usuario, id_ejemplar, ahora))
    if success:
        return True, "Reserva registrada con éxito."
    return False, result


def estaEjemplarReservado(id_ejemplar):
    """Verifica si un ejemplar tiene una reserva activa."""
    query = "SELECT idReserva FROM reservas WHERE idEjemplar = %s AND estadoReserva = 'Activa' LIMIT 1"
    success, data = fetch_query(query, (id_ejemplar,))
    if success:
        return len(data) > 0
    return False


def obtenerReservasUsuario(codigo_usuario):
    """Obtiene las reservas activas de un usuario."""
    query = """
        SELECT r.idReserva, r.idEjemplar, r.fechaReserva, l.titulo, l.autores, l.isbn
        FROM reservas r
        INNER JOIN ejemplaresfisicos ef ON ef.idEjemplar = r.idEjemplar
        INNER JOIN libros l ON l.isbn = ef.codigoIsbn
        WHERE r.codigoUsuario = %s AND r.estadoReserva = 'Activa'
        ORDER BY r.fechaReserva DESC
    """
    success, data = fetch_query(query, (codigo_usuario,))
    if success:
        return data
    return []


def cancelarReserva(id_reserva):
    """Cancela una reserva activa de un usuario."""
    query = "UPDATE reservas SET estadoReserva = 'Cancelada' WHERE idReserva = %s"
    success, result = execute_query(query, (id_reserva,))
    if success:
        return True, "Reserva cancelada."
    return False, result


def completarReserva(id_ejemplar):
    """Marca la reserva activa más antigua de un ejemplar como completada."""
    query_find = "SELECT idReserva FROM reservas WHERE idEjemplar = %s AND estadoReserva = 'Activa' ORDER BY fechaReserva ASC LIMIT 1"
    success, data = fetch_query(query_find, (id_ejemplar,))
    if success and data:
        id_reserva = data[0][0]
        query_upd = "UPDATE reservas SET estadoReserva = 'Completada' WHERE idReserva = %s"
        execute_query(query_upd, (id_reserva,))
        return True
    return False


def ampliarPrestamo(id_prestamo, dias=8):
    """Amplía la fecha de vencimiento de un préstamo activo."""
    query = "UPDATE prestamos SET fechaVencimiento = DATE_ADD(fechaVencimiento, INTERVAL %s DAY) WHERE idPrestamo = %s"
    success, result = execute_query(query, (dias, id_prestamo))
    if success:
        return True, "Préstamo ampliado con éxito."
    return False, result


def obtenerPrestamosProximosVencerUsuario(codigo_usuario):
    """Obtiene los préstamos de un usuario que vencen en los próximos 3 días y no han sido devueltos."""
    query = """
        SELECT p.idPrestamo, p.ejemplar, p.fechaVencimiento, l.titulo, l.autores
        FROM prestamos p
        INNER JOIN ejemplaresfisicos ef ON ef.idEjemplar = p.ejemplar
        INNER JOIN libros l ON l.isbn = ef.codigoIsbn
        WHERE p.codigoUsuario = %s
          AND p.estadoPrestamo = 'Aprobada'
          AND NOT EXISTS (SELECT 1 FROM devoluciones d WHERE d.idPrestamo = p.idPrestamo AND d.estadoDevolucion = 'Aprobada')
          AND p.fechaVencimiento BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 3 DAY)
        ORDER BY p.fechaVencimiento ASC
    """
    success, data = fetch_query(query, (codigo_usuario,))
    if success:
        return data
    return []


def obtenerPrestamosProximosVencerGeneral():
    """Obtiene todos los préstamos activos de la biblioteca que vencen en los próximos 3 días."""
    query = """
        SELECT p.idPrestamo, CONCAT(u.nombre, ' ', u.apellido) AS nombreUsuario, p.ejemplar, p.fechaVencimiento, l.titulo
        FROM prestamos p
        INNER JOIN usuarios u ON u.codigo = p.codigoUsuario
        INNER JOIN ejemplaresfisicos ef ON ef.idEjemplar = p.ejemplar
        INNER JOIN libros l ON l.isbn = ef.codigoIsbn
        WHERE p.estadoPrestamo = 'Aprobada'
          AND NOT EXISTS (SELECT 1 FROM devoluciones d WHERE d.idPrestamo = p.idPrestamo AND d.estadoDevolucion = 'Aprobada')
          AND p.fechaVencimiento BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 3 DAY)
        ORDER BY p.fechaVencimiento ASC
    """
    success, data = fetch_query(query)
    if success:
        return data
    return []

def procesar_y_guardar_notificaciones_automaticas():
    """Busca préstamos que vencen pronto y los registra en la tabla de notificaciones si no existen para el día actual."""
    import datetime
    prestamos_proximos = obtenerPrestamosProximosVencerGeneral()
    
    for p in prestamos_proximos:
        id_prestamo, _, ejemplar, fecha_venc, titulo = p
        
        query_user = "SELECT codigoUsuario FROM prestamos WHERE idPrestamo = %s"
        _, u_data = fetch_query(query_user, (id_prestamo,))
        
        if u_data:
            codigo_usuario = u_data[0][0]
            
            ahora = datetime.datetime.now()
            if isinstance(fecha_venc, datetime.date) and not isinstance(fecha_venc, datetime.datetime):
                fecha_venc = datetime.datetime.combine(fecha_venc, datetime.time.min)
                
            dias_restantes = max(0, (fecha_venc - ahora).days)
            fecha_formateada = fecha_venc.strftime("%d/%m/%Y")
            
            if dias_restantes == 0:
                aviso = "¡HOLA! Tu préstamo vence HOY"
            elif dias_restantes == 1:
                aviso = "Tu préstamo vence MAÑANA"
            else:
                aviso = f"Tu préstamo vence en {dias_restantes} días"

            mensaje = (
                f"⚠️ Alerta de vencimiento: {aviso}. "
                f"Libro: '{titulo}' (ejemplar {ejemplar}), "
                f"préstamo #{id_prestamo}. "
                f"Fecha límite: {fecha_formateada}. "
                "Por favor, devuélvelo a tiempo para evitar cargos adicionales."
            )
            
            # Evitar duplicar la misma notificación en el mismo día
            query_check = """
                SELECT idNotificacion FROM notificaciones 
                WHERE codigoUsuario = %s 
                  AND mensaje LIKE %s 
                  AND DATE(fechaEnvio) = CURDATE()
            """
            _, existe = fetch_query(query_check, (codigo_usuario, f"%préstamo #{id_prestamo}%"))
            
            if not existe:
                query_ins = "INSERT INTO notificaciones (codigoUsuario, mensaje, fechaEnvio, leido) VALUES (%s, %s, %s, 0)"
                execute_query(query_ins, (codigo_usuario, mensaje, ahora))
    return True
