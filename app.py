# app.py
from flask import Flask
from model.vivienda import db
from controller.vivienda_controller import vivienda_blueprint

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/precio_casas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos con la aplicación
db.init_app(app)

# Registrar el blueprint del controlador
app.register_blueprint(vivienda_blueprint)

if __name__ == '__main__':
    app.run(debug=True)