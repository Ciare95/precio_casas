import mysql.connector
import pandas as pd
import tabulate

# Conexión a la base de datos
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="precio_casas"
)

# Creamos el cursor
cursor = mydb.cursor()

# Leemos el archivo csv
df = pd.read_csv('dataset_vivienda.csv')

# Recorremos cada fila del csv
for index, row in df.iterrows():
    # Obtenemos los datos de cada fila
    precio = row['precio'] if pd.notna(row['precio']) else None
    area = row['area'] if pd.notna(row['area']) else None
    habitaciones = row['habitaciones'] if pd.notna(row['habitaciones']) else None
    antiguedad = row['antiguedad'] if pd.notna(row['antiguedad']) else None
    fecha_publicacion = row['fecha_publicacion'] if pd.notna(row['fecha_publicacion']) else None
    descripcion = row['descripcion'] if pd.notna(row['descripcion']) else None
    
    # Extraemos la primera palabra de descripción para tipo de casa
    if pd.notna(descripcion) and descripcion.split() != "":
        tipo_casa = descripcion.split()[0]
    else:
        tipo_casa = "Casa" if habitaciones > 2 else "Apartamento"
    
    # Convertimos las fechas al formato mysql (yyyy-mm-dd)
    if fecha_publicacion is not None:
        fecha_partes = fecha_publicacion.split('/')
        mes = fecha_partes[0].zfill(2)
        dia = fecha_partes[1].zfill(2)
        año = fecha_partes[2]
        fecha_mysql = f"{año}-{mes}-{dia}"
    else:
        fecha_mysql = None
    
    # Creamos la consulta sql para insertarla a la base de datos
    sql = "INSERT INTO casas (precio, area, habitaciones, antiguedad, fecha_publicacion, descripcion, tipo_casa) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    valores = (precio, area, habitaciones, antiguedad, fecha_mysql, descripcion, tipo_casa)
    
    # Ejecutamos la consulta
    cursor.execute(sql, valores)

# Ejecutamos todos los cambios
mydb.commit()

# Cerramos la conexión
cursor.close()
mydb.close()

print("Importación completada")

# Creamos la cabecera de la tabla para tabulate
table = tabulate.tabulate(
    df,
    headers=['precio','area','habitaciones','antiguedad','fecha_publicacion','descripcion'],
    tablefmt="grid"
)
