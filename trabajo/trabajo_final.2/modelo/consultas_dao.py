from .conneciondb import Conneccion


def crear_tabla():
    conn = Conneccion()

    sql = """CREATE TABLE IF NOT EXISTS Genero(
        ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        Nombre VARCHAR(50)
    );

    CREATE TABLE IF NOT EXISTS Peliculas(
        ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        Nombre VARCHAR(150),
        Duracion VARCHAR(4),
        Genero INTEGER,
        Director VARCHAR(100),
        Actor_Principal VARCHAR(100),
        FOREIGN KEY (Genero) REFERENCES Genero(ID)
    );
    """

    try:
        conn.cursor.executescript(sql)
        conn.cerrar_con()
    except Exception as e:
        print("Error creando tablas:", e)


class Peliculas:
    # Note: GUI constructs Peliculas as (nombre, duracion, genero, actor_principal, director)
    def __init__(self, nombre, duracion, genero, actor_principal, director):
        self.nombre = nombre
        self.duracion = duracion
        self.genero = genero
        self.actor_principal = actor_principal
        self.director = director

    def __str__(self):
        return f"Pelicula[{self.nombre}, {self.duracion}, {self.genero}, {self.actor_principal}, {self.director}]"


def guardar_peli(pelicula):
    conn = Conneccion()

    sql = f"""INSERT INTO Peliculas (Nombre, Duracion, Genero, Director, Actor_Principal)
        VALUES ('{pelicula.nombre}', '{pelicula.duracion}', {pelicula.genero}, '{pelicula.director}', '{pelicula.actor_principal}');"""

    try:
        conn.cursor.execute(sql)
        conn.cerrar_con()
    except Exception as e:
        print("Error guardando película:", e)


def listar_peli(condicion='todas'):
    conn = Conneccion()

    if condicion == 'todas':
        sql = """SELECT p.ID,
               p.Nombre,
               p.Duracion,
               p.Director,
               p.Actor_Principal,
               g.Nombre
        FROM Peliculas AS p
        INNER JOIN Genero AS g
          ON p.Genero = g.ID;
        """
    else:
        sql = f"""SELECT p.ID, p.Nombre, p.Duracion, p.Director, p.Actor_Principal, g.Nombre
        FROM Peliculas AS p
        INNER JOIN Genero AS g
          ON p.Genero = g.ID
        WHERE g.ID = {condicion};
        """

    try:
        conn.cursor.execute(sql)
        peliculas = conn.cursor.fetchall()
        conn.cerrar_con()
        return peliculas
    except Exception as e:
        print("Error al listar películas:", e)
        return []


def listar_generos():
    conn = Conneccion()

    sql = "SELECT ID, Nombre FROM Genero ORDER BY Nombre;"

    try:
        conn.cursor.execute(sql)
        resultados = conn.cursor.fetchall()
        conn.cerrar_con()
        return resultados
    except Exception as e:
        print("Error al listar géneros:", e)
        return []


def editar_peli(pelicula, id):
    conn = Conneccion()

    sql = f"""UPDATE Peliculas
        SET Nombre = '{pelicula.nombre}',
            Duracion = '{pelicula.duracion}',
            Genero = {pelicula.genero},
            Director = '{pelicula.director}',
            Actor_Principal = '{pelicula.actor_principal}'
        WHERE ID = {id};"""

    try:
        conn.cursor.execute(sql)
        conn.cerrar_con()
    except Exception as e:
        print("Error al editar película:", e)


def borrar_peli(id):
    conn = Conneccion()

    sql = f"DELETE FROM Peliculas WHERE ID = {id};"

    try:
        conn.cursor.execute(sql)
        conn.cerrar_con()
    except Exception as e:
        print("Error al borrar película:", e)
