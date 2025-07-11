import mysql.connector

def get_db_connection():
    """Establece una conexión con la base de datos."""
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="precio_casas"
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Error al conectar con la base de datos: {err}")
        return None
