from modelo import obtener_viviendas, precio_metro_cuadrado, obtener_habitaciones
from controlador import vivienda_clasificacion
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

#print()
#print(f"Total de viviendas:{len(obtener_viviendas())}")
#print()
#print(f"Precio promedio por metro cuadrado: ${precio_metro_cuadrado():,.0f} COP")
#print()
#vivienda_clasificacion()

def habitaciones_numero():
    habitaciones = obtener_habitaciones()
    for h in habitaciones['habitaciones']:
        print(h)

habitaciones_numero()