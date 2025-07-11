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

# Leemos el archivo csv
df = pd.read_csv('dataset_vivienda.csv')

# Creamos la cabecera de la tabla para tabulate
table = tabulate.tabulate(
    df,
    headers=['precio','area','habitaciones','antiguedad','fecha_publicacion','descripcion'],
    tablefmt="grid"
)

print(mydb)