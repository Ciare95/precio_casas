from importer import import_data_from_csv

if __name__ == "__main__":
    # Ruta al archivo CSV que se va a importar
    csv_filepath = 'dataset_vivienda.csv'
    
    # Llama a la función de importación
    import_data_from_csv(csv_filepath)
