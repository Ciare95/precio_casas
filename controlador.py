from modelo import obtener_precio, obtener_viviendas, obtener_clasificacion
from database import obtener_conexion
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

engine = create_engine("mysql+pymysql://root:@localhost/precio_casas")
mydb = obtener_conexion()

def suma_precios():
    
    df_precios = obtener_precio()

    if df_precios is not None and not df_precios.empty:
        suma_precios = df_precios['precio'].sum()
    else:
        print("No se encontraron precios.")
    
    return suma_precios


def vivienda_clasificacion():
    """total de viviendas por tipo de vivienda"""
    if not mydb:
        return
    
    try:
        viviendas = obtener_viviendas()
        print("===Tipos de vivienda===")
        descripciones = obtener_clasificacion()
        print()
        print("Clasificación de vivienda por tipo: \n")
            
        for tipo in descripciones:
            cantidad = viviendas[viviendas['descripcion'] == tipo].shape[0]
            print(f"Tipo: {tipo} - Cantidad de viviendas: {cantidad}")
    
    except Exception as e:
        print(f"Ocurrió un error en el método obtener clasificación: {e}")
        if mydb.is_connected():
            mydb.rollback()
    finally:
        if mydb.is_connected():
            mydb.close()
            print("Conexión a la base de datos cerrada.")
