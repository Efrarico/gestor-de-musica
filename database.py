import sqlite3
from typing import Optional, List, Tuple, Dict, Any
from config import DATABASE_NAME

def conectar(db_path: Optional[str] = None):
    """Obtiene una conexión a la base de datos SQLite."""
    return sqlite3.connect(db_path or DATABASE_NAME)

def crear_tablas(db_path: Optional[str] = None) -> None:
    conn = conectar(db_path)
    cur = conn.cursor()
    # Tabla artistas
    cur.execute('''
        CREATE TABLE IF NOT EXISTS artistas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
    ''')
    # Tabla albums
    cur.execute('''
        CREATE TABLE IF NOT EXISTS albums (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            artista_id INTEGER NOT NULL,
            anio INTEGER,
            UNIQUE(titulo, artista_id),
            FOREIGN KEY(artista_id) REFERENCES artistas(id) ON DELETE CASCADE
        )
    ''')
    # Tabla canciones
    cur.execute('''
        CREATE TABLE IF NOT EXISTS canciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            artista_id INTEGER NOT NULL,
            album_id INTEGER,
            genero TEXT,
            duracion TEXT,  -- mm:ss
            anio INTEGER,
            UNIQUE(titulo, artista_id),
            FOREIGN KEY(artista_id) REFERENCES artistas(id) ON DELETE CASCADE,
            FOREIGN KEY(album_id) REFERENCES albums(id) ON DELETE SET NULL
        )
    ''')
    conn.commit()
    conn.close()

# -------- ARTISTAS CRUD --------
def crear_artista(nombre: str, db_path: Optional[str] = None) -> int:
    conn = conectar(db_path)
    cur = conn.cursor()
    cur.execute("INSERT INTO artistas (nombre) VALUES (?)", (nombre.strip(),))
    conn.commit()
    artist_id = cur.lastrowid
    conn.close()
    return artist_id

def obtener_artistas(db_path: Optional[str] = None) -> List[Tuple]:
    conn = conectar(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, nombre FROM artistas ORDER BY nombre ASC")
    rows = cur.fetchall()
    conn.close()
    return rows

def actualizar_artista(artista_id: int, nombre: str, db_path: Optional[str] = None) -> None:
    conn = conectar(db_path)
    cur = conn.cursor()
    cur.execute("UPDATE artistas SET nombre=? WHERE id=?", (nombre.strip(), artista_id))
    conn.commit()
    conn.close()

def eliminar_artista(artista_id: int, db_path: Optional[str] = None) -> None:
    conn = conectar(db_path)
    cur = conn.cursor()
    cur.execute("DELETE FROM artistas WHERE id=?", (artista_id,))
    conn.commit()
    conn.close()

def buscar_artista_por_nombre(nombre: str, db_path: Optional[str] = None) -> Optional[Tuple[int, str]]:
    conn = conectar(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, nombre FROM artistas WHERE nombre = ?", (nombre.strip(),))
    row = cur.fetchone()
    conn.close()
    return row

# -------- ALBUMS CRUD --------
def crear_album(titulo: str, artista_id: int, anio: Optional[int], db_path: Optional[str] = None) -> int:
    conn = conectar(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO albums (titulo, artista_id, anio) VALUES (?, ?, ?)",
        (titulo.strip(), artista_id, anio)
    )
    conn.commit()
    album_id = cur.lastrowid
    conn.close()
    return album_id

def obtener_albums(db_path: Optional[str] = None) -> List[Tuple]:
    conn = conectar(db_path)
    cur = conn.cursor()
    cur.execute('''
        SELECT albums.id, albums.titulo, artistas.nombre, albums.anio
        FROM albums
        JOIN artistas ON albums.artista_id = artistas.id
        ORDER BY albums.titulo ASC
    ''')
    rows = cur.fetchall()
    conn.close()
    return rows

def actualizar_album(album_id: int, titulo: str, artista_id: int, anio: Optional[int], db_path: Optional[str] = None) -> None:
    conn = conectar(db_path)
    cur = conn.cursor()
    cur.execute("UPDATE albums SET titulo=?, artista_id=?, anio=? WHERE id=?", (titulo.strip(), artista_id, anio, album_id))
    conn.commit()
    conn.close()

def eliminar_album(album_id: int, db_path: Optional[str] = None) -> None:
    conn = conectar(db_path)
    cur = conn.cursor()
    cur.execute("DELETE FROM albums WHERE id=?", (album_id,))
    conn.commit()
    conn.close()

# -------- CANCIONES CRUD --------
def crear_cancion(titulo: str, artista_id: int, album_id: Optional[int], genero: Optional[str],
                  duracion: Optional[str], anio: Optional[int], db_path: Optional[str] = None) -> int:
    conn = conectar(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO canciones (titulo, artista_id, album_id, genero, duracion, anio) VALUES (?, ?, ?, ?, ?, ?)",
        (titulo.strip(), artista_id, album_id, genero, duracion, anio)
    )
    conn.commit()
    song_id = cur.lastrowid
    conn.close()
    return song_id

def obtener_canciones(db_path: Optional[str] = None) -> List[Tuple]:
    conn = conectar(db_path)
    cur = conn.cursor()
    cur.execute('''
        SELECT canciones.id, canciones.titulo, artistas.nombre AS artista, 
               COALESCE(albums.titulo, '') AS album, canciones.genero, canciones.duracion, canciones.anio
        FROM canciones
        JOIN artistas ON canciones.artista_id = artistas.id
        LEFT JOIN albums ON canciones.album_id = albums.id
        ORDER BY canciones.titulo ASC
    ''')
    rows = cur.fetchall()
    conn.close()
    return rows

def actualizar_cancion(cancion_id: int, titulo: str, artista_id: int, album_id: Optional[int],
                       genero: Optional[str], duracion: Optional[str], anio: Optional[int], db_path: Optional[str] = None) -> None:
    conn = conectar(db_path)
    cur = conn.cursor()
    cur.execute('''
        UPDATE canciones
        SET titulo=?, artista_id=?, album_id=?, genero=?, duracion=?, anio=?
        WHERE id=?
    ''', (titulo.strip(), artista_id, album_id, genero, duracion, anio, cancion_id))
    conn.commit()
    conn.close()

def eliminar_cancion(cancion_id: int, db_path: Optional[str] = None) -> None:
    conn = conectar(db_path)
    cur = conn.cursor()
    cur.execute("DELETE FROM canciones WHERE id=?", (cancion_id,))
    conn.commit()
    conn.close()

# Utilidades
def obtener_artista_por_id(artista_id: int, db_path: Optional[str] = None) -> Optional[Tuple]:
    conn = conectar(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, nombre FROM artistas WHERE id=?", (artista_id,))
    row = cur.fetchone()
    conn.close()
    return row

def obtener_album_por_id(album_id: int, db_path: Optional[str] = None) -> Optional[Tuple]:
    conn = conectar(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, titulo, artista_id, anio FROM albums WHERE id=?", (album_id,))
    row = cur.fetchone()
    conn.close()
    return row
