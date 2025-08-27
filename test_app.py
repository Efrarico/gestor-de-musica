import os
import tempfile
import unittest
import database as db
import validaciones as v

class TestGestorMusica(unittest.TestCase):
    def setUp(self):
        # Usar una base temporal por test
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmp.name, "test.db")
        db.crear_tablas(self.db_path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_validaciones_basicas(self):
        self.assertTrue(v.validar_nombre("Queen"))
        self.assertFalse(v.validar_nombre("   "))
        self.assertTrue(v.validar_duracion("3:45"))
        self.assertFalse(v.validar_duracion("3:78"))
        self.assertTrue(v.validar_anio("1999"))
        self.assertFalse(v.validar_anio("abc"))

    def test_crud_artist_album_song(self):
        # Crear artista
        art_id = db.crear_artista("Queen", self.db_path)
        self.assertIsInstance(art_id, int)
        # Crear álbum
        alb_id = db.crear_album("A Night at the Opera", art_id, 1975, self.db_path)
        self.assertIsInstance(alb_id, int)
        # Crear canción
        can_id = db.crear_cancion("Bohemian Rhapsody", art_id, alb_id, "Rock", "5:55", 1975, self.db_path)
        self.assertIsInstance(can_id, int)

        # Leer
        artistas = db.obtener_artistas(self.db_path)
        self.assertEqual(len(artistas), 1)
        albums = db.obtener_albums(self.db_path)
        self.assertEqual(len(albums), 1)
        canciones = db.obtener_canciones(self.db_path)
        self.assertEqual(len(canciones), 1)

        # Update
        db.actualizar_artista(art_id, "Queen (UK)", self.db_path)
        db.actualizar_album(alb_id, "A Night at the Opera (Remastered)", art_id, 2011, self.db_path)
        db.actualizar_cancion(can_id, "Bohemian Rhapsody - Remaster", art_id, alb_id, "Rock", "5:55", 2011, self.db_path)

        # Delete
        db.eliminar_cancion(can_id, self.db_path)
        self.assertEqual(len(db.obtener_canciones(self.db_path)), 0)
        db.eliminar_album(alb_id, self.db_path)
        self.assertEqual(len(db.obtener_albums(self.db_path)), 0)
        db.eliminar_artista(art_id, self.db_path)
        self.assertEqual(len(db.obtener_artistas(self.db_path)), 0)

if __name__ == '__main__':
    unittest.main()
