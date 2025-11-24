import sqlite3
import os

class Conneccion():
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))  # project root /TrabajoFinal.1/modelo -> parent is project root
        db_folder = os.path.join(base_dir, 'ddbb')
        os.makedirs(db_folder, exist_ok=True)
        self.base_datos = os.path.join(db_folder, 'peliculas.db')
        self.conexion = sqlite3.connect(self.base_datos)
        self.cursor = self.conexion.cursor()

    def cerrar_con(self):
        try:
            self.conexion.commit()
        finally:
            self.conexion.close()
