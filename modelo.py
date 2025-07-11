from database import obtener_conexion
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:@localhost/precio_casas")
mydb = obtener_conexion()

def obtener_viviendas():
    """Muestra el total de viviendas en el sistema"""
    if not mydb:
        return
    
    try:
        df = pd.read_sql_query("SELECT * FROM casas", con=engine)
        return df
    except Exception as e:
        print(f"Ocurrió un error en la vista total de viviendas: {e}")
        if mydb.is_connected():
            mydb.rollback()
    finally:
        if mydb.is_connected():
            mydb.close()
            print("Conexión a la base de datos cerrada.")
            
            
def obtener_precio():
    """Obtener el precio de cada vivienda"""
    if not mydb:
        return
    
    try:
        df_precios = pd.read_sql_query("SELECT precio FROM casas", con=engine)
        return df_precios
    except Exception as e:
        print(f"Ocurrió un error en la vista total de viviendas: {e}")
        if mydb.is_connected():
            mydb.rollback()
    finally:
        if mydb.is_connected():
            mydb.close()
            print("Conexión a la base de datos cerrada.")
            
            
def obtener_area():
    """Se obtiene el area de cada vivienda"""
    if not mydb:
        return
    
    try:
        df_area = pd.read_sql_query("SELECT area FROM casas", con=engine)
        return df_area
    except Exception as e:
        print(f"Ocurrió un error en la vista total de viviendas: {e}")
        if mydb.is_connected():
            mydb.rollback()
    finally:
        if mydb.is_connected():
            mydb.close()
            print("Conexión a la base de datos cerrada.")
            
            
def precio_metro_cuadrado():
    """promedio del precio por metro cuadrado de la vivienda en la región"""
    if not mydb:
        return
    
    try:
        precios = obtener_precio()
        areas = obtener_area()
        totalViviendas = len(obtener_viviendas())
        
        precioMetroCuadrado = precios['precio'] / areas['area']
        promedioMetroCuadrado = sum(precioMetroCuadrado) / totalViviendas
        return promedioMetroCuadrado
    
    except Exception as e:
        print(f"Ocurrió un error en la vista total de viviendas: {e}")
        if mydb.is_connected():
            mydb.rollback()
    finally:
        if mydb.is_connected():
            mydb.close()
            print("Conexión a la base de datos cerrada.")
            
            
def obtener_clasificacion():
    """Se obtiene la clasificación de la vivienda según su descripción"""
    if not mydb:
        return
    
    try:
        df_descripcion = pd.read_sql("SELECT descripcion from casas", con=engine)
        descripcionesUnicas = df_descripcion['descripcion'].dropna().unique()
        for desc in descripcionesUnicas:
            print(f"- {desc}")
        
        return descripcionesUnicas     
            
    
    except Exception as e:
        print(f"Ocurrió un error en el método obtener clasificación: {e}")
        if mydb.is_connected():
            mydb.rollback()
    finally:
        if mydb.is_connected():
            mydb.close()
            print("Conexión a la base de datos cerrada.")

def obtener_habitaciones():
    """Obtenemos las habitaciones de cada vivienda"""
    if not mydb:
        return
    
    try:
        df_habitaciones = pd.read_sql("SELECT habitaciones FROM casas", con=engine)
        return df_habitaciones
    
    except Exception as e:
        print(f"Ocurrió un error en el método obtener habitaciones: {e}")
        if mydb.is_connected():
            mydb.rollback()
    finally:
        if mydb.is_connected():
            mydb.close()
            print("Conexión a la base de datos cerrada.")
            
def obtener_antiguedad():
    """Obtenemos los años de antiguedad de cada vivienda"""
    if not mydb:
        return
    
    try:
        pass
    
    except Exception as e:
        print(f"Ocurrió un error en el método obtener habitaciones: {e}")
        if mydb.is_connected():
            mydb.rollback()
    finally:
        if mydb.is_connected():
            mydb.close()
            print("Conexión a la base de datos cerrada.")