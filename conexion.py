import mysql.connector

try :
    connection = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'abcbc6f5',
        db = 'biblioGestor'
    )
    if connection.is_connected():
        print('Conexion exitosa a la base de datos')
        info_server = connection.server_info
        print('Version del servidor MySQL: ', info_server)
        cursor = connection.cursor()
        cursor.execute('SELECT DATABASE();')
        record = cursor.fetchone()
        print('Conectado a la base de datos: ', record)
except Exception as ex:
    print(ex)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print('Conexion a la base de datos cerrada')