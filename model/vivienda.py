from flask_sqlalchemy import SQLAlchemy

# Crear instancia de SQLAlchemy
db = SQLAlchemy()

class Vivienda(db.Model):
    __tablename__ = 'casas'
    id = db.Column(db.Integer, primary_key=True)
    precio = db.Column(db.Float)
    area = db.Column(db.Float)
    habitaciones = db.Column(db.Integer)
    antiguedad = db.Column(db.Integer)
    descripcion = db.Column(db.String(255))
    fecha_publicacion = db.Column(db.Date)