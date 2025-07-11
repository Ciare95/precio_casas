from database import obtener_conexion
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:@localhost/precio_casas")

def total_viviendas():
    """Muestra el total de viviendas en el sistema"""
    mydb = obtener_conexion()
    if not mydb:
        return
    
    try:
        df = pd.read_sql_query("SELECT * FROM casas", con=engine)
        return len(df)
    except Exception as e:
        print(f"Ocurrió un error en la vista total de viviendas: {e}")
        if mydb.is_connected():
            mydb.rollback()
    finally:
        if mydb.is_connected():
            mydb.close()
            print("Conexión a la base de datos cerrada.")
        

