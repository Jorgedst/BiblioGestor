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

def validarUserCodigo(codigo):
    query = "SELECT * FROM usuarios WHERE codigo = %s"
    success, data = fetch_query(query, (codigo,))
    if success:
        return len(data) > 0, data
    else:
        return False, data

def validarUserIdentificacion(id):
    query = "SELECT * FROM usuarios WHERE identificación = %s"
    success, data = fetch_query(query, (id,))
    if success:
        return len(data) > 0, data
    else:
        return False, data

def obtenerNombreUsuario(id):
    query = "SELECT nombre FROM usuarios WHERE codigo = %s"
    success, data = fetch_query(query, (id,))
    if success and data:
        return data[0][0]
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
