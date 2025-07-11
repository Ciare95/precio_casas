from importer import importar_csv

if __name__ == "__main__":
    # Ruta al archivo CSV que se va a importar
    csv_filepath = 'dataset_vivienda.csv'
    
    # Llama a la función de importación
    importar_csv(csv_filepath)
