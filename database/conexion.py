import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()  # carga el .env

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT"))
        )
        return connection
    except Exception as ex:
        print("Error de conexión:", ex)
        return None