import mysql.connector
def get_connection():
    try :
        connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'abcbc6f5',
            db = 'biblioGestor'
        )
        return connection
    except Exception as ex:
        print("Error de conexión: ",ex)
        return None