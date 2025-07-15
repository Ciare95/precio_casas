from flask import Blueprint, render_template
from model.vivienda import Vivienda
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Para generar gráficos sin interfaz gráfica
from sklearn.linear_model import LinearRegression
import numpy as np
import io
import base64

# Configurar matplotlib
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14

# Crear el blueprint
vivienda_blueprint = Blueprint('vivienda', __name__)

@vivienda_blueprint.route('/')
def home():
    """Página principal con análisis de precio vs valor metro cuadrado por tipo"""
    
    # Obtener datos de la base de datos
    viviendas = Vivienda.query.all()
    
    # Preparar los datos para el modelo 
    datos_procesados = procesar_datos_viviendas(viviendas)
    
    # Verificar que tengamos datos
    if len(datos_procesados) == 0:
        return "No hay datos suficientes para el análisis"
    
    # Entrenar el modelo de regresión lineal
    datos_modelo = entrenar_modelo_regresion_metro_cuadrado(datos_procesados)
    
    # Generar el gráfico
    grafico_base64 = generar_grafico_dispersion(datos_procesados, datos_modelo)
    
    # Agregar el gráfico a los datos
    datos_modelo['grafico'] = grafico_base64
    
    return render_template('regresion.html', datos=datos_modelo)

@vivienda_blueprint.route('/prediccion')
def prediccion():
    """Página para hacer predicciones"""
    return render_template('prediccion.html')

@vivienda_blueprint.route('/calcular_precio/<precio>')
def calcular_precio(precio):
    """Calcular valor por m² basado en precio"""
    
    # Convertir precio a float
    try:
        precio = float(precio)
    except (ValueError, TypeError):
        return "Precio inválido", 400
    
    # Obtener datos y entrenar modelo
    viviendas = Vivienda.query.all()
    datos_procesados = procesar_datos_viviendas(viviendas)
    
    if len(datos_procesados) == 0:
        return "No hay datos suficientes"
    
    # Entrenar modelo - PRECIO como X, VALOR_M2 como Y
    precios = [dato['precio'] for dato in datos_procesados]
    valores_m2 = [dato['valor_m2'] for dato in datos_procesados]
    
    X = np.array(precios).reshape(-1, 1)
    y = np.array(valores_m2)
    
    modelo = LinearRegression()
    modelo.fit(X, y)
    
    # Hacer predicción
    precio_prediccion = np.array([[precio]])
    valor_m2_predicho = modelo.predict(precio_prediccion)[0]
    
    resultado = {
        'precio': precio,
        'valor_m2_predicho': valor_m2_predicho,
        'intercepto': modelo.intercept_,
        'pendiente': modelo.coef_[0]
    }
    
    return render_template('resultado.html', resultado=resultado)

def procesar_datos_viviendas(viviendas):
    """Procesar datos de viviendas para obtener valor por m² y tipo de casa"""
    
    datos_procesados = []
    
    for vivienda in viviendas:
        # Verificar que tengamos precio y área válidos
        if vivienda.precio is not None and vivienda.area is not None and vivienda.area > 0:
            
            # Calcular valor por metro cuadrado
            valor_m2 = vivienda.precio / vivienda.area
            
            # Determinar tipo de casa
            tipo_casa = determinar_tipo_casa(vivienda.descripcion, vivienda.habitaciones)
            
            # Agregar datos procesados
            datos_procesados.append({
                'precio': vivienda.precio,
                'area': vivienda.area,
                'valor_m2': valor_m2,
                'tipo_casa': tipo_casa,
                'habitaciones': vivienda.habitaciones,
                'antiguedad': vivienda.antiguedad
            })
    
    return datos_procesados

def determinar_tipo_casa(descripcion, habitaciones):
    """Determinar tipo de casa basado en descripción o número de habitaciones"""
    
    # Si la descripción existe y no está vacía
    if descripcion and descripcion.strip():
        # Obtener la primera palabra de la descripción
        primera_palabra = descripcion.strip().split()[0]
        return primera_palabra
    else:
        # Si no hay descripción, usar lógica de habitaciones
        if habitaciones is not None and habitaciones > 2:
            return "Casa"
        else:
            return "Apartamento"

def entrenar_modelo_regresion_metro_cuadrado(datos_procesados):
    """Función para entrenar el modelo de regresión lineal con precio como X y valor por m² como Y"""
    
    # Extraer precios y valores por m²
    precios = [dato['precio'] for dato in datos_procesados]
    valores_m2 = [dato['valor_m2'] for dato in datos_procesados]
    
    # Convertir a arrays de numpy - PRECIO como X, VALOR_M2 como Y
    X = np.array(precios).reshape(-1, 1)
    y = np.array(valores_m2)
    
    # Crear y entrenar el modelo
    modelo = LinearRegression()
    modelo.fit(X, y)
    
    # Obtener coeficientes
    intercepto = modelo.intercept_
    pendiente = modelo.coef_[0]
    r_cuadrado = modelo.score(X, y)
    
    # Calcular estadísticas usando bucles simples
    total_datos = len(datos_procesados)
    precio_promedio = 0
    valor_m2_promedio = 0
    
    # Calcular promedio de precios
    for precio in precios:
        precio_promedio = precio_promedio + precio
    precio_promedio = precio_promedio / len(precios)
    
    # Calcular promedio de valores por m²
    for valor in valores_m2:
        valor_m2_promedio = valor_m2_promedio + valor
    valor_m2_promedio = valor_m2_promedio / len(valores_m2)
    
    # Calcular estadísticas por tipo de casa
    estadisticas_tipo = calcular_estadisticas_por_tipo(datos_procesados)
    
    # Retornar datos del modelo
    datos_modelo = {
        'intercepto': intercepto,
        'pendiente': pendiente,
        'r_cuadrado': r_cuadrado,
        'total_datos': total_datos,
        'precio_promedio': precio_promedio,
        'valor_m2_promedio': valor_m2_promedio,
        'estadisticas_tipo': estadisticas_tipo
    }
    
    return datos_modelo

def calcular_estadisticas_por_tipo(datos_procesados):
    """Calcular estadísticas por tipo de casa"""
    
    # Diccionario para almacenar datos por tipo
    tipos_datos = {}
    
    # Agrupar datos por tipo
    for dato in datos_procesados:
        tipo = dato['tipo_casa']
        if tipo not in tipos_datos:
            tipos_datos[tipo] = {
                'precios': [],
                'valores_m2': [],
                'count': 0
            }
        
        tipos_datos[tipo]['precios'].append(dato['precio'])
        tipos_datos[tipo]['valores_m2'].append(dato['valor_m2'])
        tipos_datos[tipo]['count'] += 1
    
    # Calcular estadísticas para cada tipo
    estadisticas = {}
    for tipo, datos in tipos_datos.items():
        precio_promedio = sum(datos['precios']) / len(datos['precios'])
        valor_m2_promedio = sum(datos['valores_m2']) / len(datos['valores_m2'])
        
        estadisticas[tipo] = {
            'count': datos['count'],
            'precio_promedio': precio_promedio,
            'valor_m2_promedio': valor_m2_promedio
        }
    
    return estadisticas

def generar_grafico_dispersion(datos_procesados, datos_modelo):
    """Función para generar el gráfico de dispersión precio vs valor por m² por tipo"""
    
    # Separar datos por tipo de casa
    tipos_datos = {}
    for dato in datos_procesados:
        tipo = dato['tipo_casa']
        if tipo not in tipos_datos:
            tipos_datos[tipo] = {
                'precios': [],
                'valores_m2': []
            }
        tipos_datos[tipo]['precios'].append(dato['precio'])
        tipos_datos[tipo]['valores_m2'].append(dato['valor_m2'])
    
    # Crear el gráfico
    plt.figure(figsize=(12, 8))
    
    # Colores para diferentes tipos
    colores = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
    color_idx = 0
    
    # Graficar puntos para cada tipo - PRECIO en X, VALOR_M2 en Y
    for tipo, datos in tipos_datos.items():
        color = colores[color_idx % len(colores)]
        plt.scatter(datos['precios'], datos['valores_m2'], 
                color=color, alpha=0.6, label=f'{tipo} ({len(datos["precios"])} propiedades)')
        color_idx += 1
    
    # Línea de regresión general
    precios_todos = [dato['precio'] for dato in datos_procesados]
    valores_m2_todos = [dato['valor_m2'] for dato in datos_procesados]
    
    precio_min = min(precios_todos)
    precio_max = max(precios_todos)
    
    # Crear puntos para la línea de regresión
    precios_linea = np.linspace(precio_min, precio_max, 100)
    valores_m2_linea = []
    
    for precio in precios_linea:
        valor_m2_calculado = datos_modelo['intercepto'] + datos_modelo['pendiente'] * precio
        valores_m2_linea.append(valor_m2_calculado)
    
    # Línea de regresión
    plt.plot(precios_linea, valores_m2_linea, color='black', linewidth=2, 
             linestyle='--', label='Línea de regresión general')
    
    # Configurar el gráfico - PRECIO en X, VALOR_M2 en Y
    plt.xlabel('Precio Total ($)')
    plt.ylabel('Valor por Metro Cuadrado ($/m²)')
    plt.title('Análisis de Valor por Metro Cuadrado vs Precio Total por Tipo de Vivienda')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    
    # Formato de números en los ejes
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Convertir el gráfico a base64
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
    img_buffer.seek(0)
    
    # Codificar en base64
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    
    # Cerrar el plot
    plt.close()
    
    return img_base64
