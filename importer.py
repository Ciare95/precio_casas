import pandas as pd
from database import get_db_connection

def check_if_record_exists(cursor, values):
    """Verifica si un registro ya existe en la base de datos."""
    sql = "SELECT COUNT(*) FROM casas WHERE precio = %s AND area = %s AND habitaciones = %s AND antiguedad = %s AND fecha_publicacion = %s AND descripcion = %s"
    # Adaptar los valores para la consulta de verificación
    check_values = (values[0], values[1], values[2], values[3], values[4], values[5])
    cursor.execute(sql, check_values)
    return cursor.fetchone()[0] > 0

def import_data_from_csv(filepath):
    """Lee un archivo CSV e importa los datos a la base de datos."""
    mydb = get_db_connection()
    if not mydb:
        return

    try:
        cursor = mydb.cursor()
        df = pd.read_csv(filepath)

        for index, row in df.iterrows():
            precio = row['precio'] if pd.notna(row['precio']) else None
            area = row['area'] if pd.notna(row['area']) else None
            habitaciones = row['habitaciones'] if pd.notna(row['habitaciones']) else None
            antiguedad = row['antiguedad'] if pd.notna(row['antiguedad']) else None
            fecha_publicacion = row['fecha_publicacion'] if pd.notna(row['fecha_publicacion']) else None
            descripcion = row['descripcion'] if pd.notna(row['descripcion']) else None

            if pd.notna(descripcion) and descripcion.split():
                tipo_casa = descripcion.split()[0]
            else:
                tipo_casa = "Casa" if habitaciones and habitaciones > 2 else "Apartamento"

            fecha_mysql = None
            if fecha_publicacion:
                try:
                    fecha_partes = fecha_publicacion.split('/')
                    if len(fecha_partes) == 3:
                        mes = fecha_partes[0].zfill(2)
                        dia = fecha_partes[1].zfill(2)
                        año = fecha_partes[2]
                        fecha_mysql = f"{año}-{mes}-{dia}"
                except Exception:
                    fecha_mysql = None
            
            valores = (precio, area, habitaciones, antiguedad, fecha_mysql, descripcion, tipo_casa)

            if not check_if_record_exists(cursor, valores):
                sql = "INSERT INTO casas (precio, area, habitaciones, antiguedad, fecha_publicacion, descripcion, tipo_casa) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, valores)
                print(f"Insertando nuevo registro: {valores}")
            else:
                print(f"Registro duplicado omitido: {valores}")


        mydb.commit()
        print("Importación completada.")

    except Exception as e:
        print(f"Ocurrió un error durante la importación: {e}")
        if mydb.is_connected():
            mydb.rollback()
    finally:
        if mydb.is_connected():
            cursor.close()
            mydb.close()
            print("Conexión a la base de datos cerrada.")
