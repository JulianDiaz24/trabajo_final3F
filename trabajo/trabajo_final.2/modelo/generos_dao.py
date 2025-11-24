from .consultas_dao import listar_generos

class GeneroManager:
    def __init__(self):
        self.generos = []
        self.cargar_generos()
    
    def cargar_generos(self):
        x = listar_generos()
        self.generos = [{'id': 0, 'Nombre': 'Seleccione Uno'}]
        for genero in x:
            self.generos.append({'id': genero[0], 'Nombre': genero[1]})
    
    def get_nombres(self):
        return [genero['Nombre'] for genero in self.generos]
    
    def get_id_por_indice(self, index):
        if 0 <= index < len(self.generos):
            return self.generos[index]['id']
        return None
    
    def get_id_por_nombre(self, nombre):
        for genero in self.generos:
            if genero['Nombre'] == nombre:
                return genero['id']
        return None
    
    def get_indice_por_nombre(self, nombre):
        for i, genero in enumerate(self.generos):
            if genero['Nombre'] == nombre:
                return i
        return 0
