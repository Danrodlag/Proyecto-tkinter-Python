# Aquí esta el manejo de la base de datos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, REAL, Boolean

# Primero creamos el engine para crear y conectarnos a la base de datos
engine =create_engine("sqlite:///database/productos.db", connect_args={"check_same_thread": False})

# Ahora conectamos para poder mandarle ordenes a la base de datos
Session = sessionmaker(bind=engine)
session = Session()
# Sesion lanzada

# Ahora para mapear las clases a tablas
Base = declarative_base()


class Producto(Base):

    __tablename__ = "producto"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    precio = Column(REAL, nullable=False)
    categoria = Column(String(200), nullable=False)
    stock = Column(Boolean, nullable=False)

    def __init__(self, nombre, precio, categoria, stock):
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.stock = stock

    def __str__(self):
        return "{} {} {} {}".format(self.nombre, self.precio, self.categoria, self.stock)
