import sys
from typing import Optional
import database as db
import validaciones as v
from config import GENRES

SEP = "-" * 60

def _input(msg: str) -> str:
    try:
        return input(msg)
    except EOFError:
        print("\nEntrada finalizada.")
        sys.exit(0)

def pausar():
    _input("\nPresiona Enter para continuar...")

def seleccionar_genero() -> Optional[str]:
    print("Géneros disponibles:")
    for i, g in enumerate(GENRES, start=1):
        print(f"  {i}. {g}")
    eleccion = _input("Selecciona número de género (o vacío para omitir): ").strip()
    if not eleccion:
        return None
    try:
        idx = int(eleccion)
        if 1 <= idx <= len(GENRES):
            return GENRES[idx - 1]
    except Exception:
        pass
    print("Selección inválida.")
    return None

def menu_principal() -> str:
    print("\n🎵 Gestor de Música")
    print(SEP)
    print("1. Artistas")
    print("2. Álbums")
    print("3. Canciones")
    print("4. Salir")
    return _input("Elige una opción: ").strip()

# ------------- MENÚ ARTISTAS -------------
def menu_artistas():
    while True:
        print("\n👤 Artistas")
        print(SEP)
        print("1. Agregar artista")
        print("2. Ver artistas")
        print("3. Editar artista")
        print("4. Eliminar artista")
        print("5. Regresar")
        op = _input("Opción: ").strip()
        if op == "1":
            nombre = _input("Nombre del artista: ").strip()
            if not v.validar_nombre(nombre):
                print("❌ Nombre inválido.")
                continue
            try:
                db.crear_artista(nombre)
                print("✅ Artista agregado.")
            except Exception as e:
                print(f"❌ Error: {e}")
            pausar()
        elif op == "2":
            artistas = db.obtener_artistas()
            if not artistas:
                print("Sin artistas registrados.")
            else:
                print(SEP)
                for a in artistas:
                    print(f"[{a[0]}] {a[1]}")
            pausar()
        elif op == "3":
            try:
                art_id = int(_input("ID del artista a editar: "))
                nombre = _input("Nuevo nombre: ").strip()
                if not v.validar_nombre(nombre):
                    print("❌ Nombre inválido.")
                    continue
                db.actualizar_artista(art_id, nombre)
                print("✅ Artista actualizado.")
            except Exception as e:
                print(f"❌ Error: {e}")
            pausar()
        elif op == "4":
            try:
                art_id = int(_input("ID del artista a eliminar: "))
                db.eliminar_artista(art_id)
                print("✅ Artista eliminado.")
            except Exception as e:
                print(f"❌ Error: {e}")
            pausar()
        elif op == "5":
            return
        else:
            print("Opción inválida.")

# ------------- MENÚ ÁLBUMS -------------
def _listar_artistas_select() -> Optional[int]:
    artistas = db.obtener_artistas()
    if not artistas:
        print("Primero agrega artistas.")
        return None
    for a in artistas:
        print(f"[{a[0]}] {a[1]}")
    try:
        sel = int(_input("ID de artista: "))
        return sel
    except Exception:
        print("Selección inválida.")
        return None

def menu_albums():
    while True:
        print("\n💿 Álbums")
        print(SEP)
        print("1. Agregar álbum")
        print("2. Ver álbums")
        print("3. Editar álbum")
        print("4. Eliminar álbum")
        print("5. Regresar")
        op = _input("Opción: ").strip()
        if op == "1":
            artista_id = _listar_artistas_select()
            if not artista_id:
                pausar(); continue
            titulo = _input("Título del álbum: ").strip()
            if not v.validar_nombre(titulo):
                print("❌ Título inválido."); pausar(); continue
            anio = _input("Año (opcional): ").strip()
            if anio and not v.validar_anio(anio):
                print("❌ Año inválido."); pausar(); continue
            try:
                db.crear_album(titulo, artista_id, v.normalizar_anio(anio))
                print("✅ Álbum agregado.")
            except Exception as e:
                print(f"❌ Error: {e}")
            pausar()
        elif op == "2":
            rows = db.obtener_albums()
            if not rows:
                print("Sin álbums registrados.")
            else:
                print(SEP)
                for r in rows:
                    print(f"[{r[0]}] {r[1]} — {r[2]} ({r[3] if r[3] else 's/f'})")
            pausar()
        elif op == "3":
            try:
                alb_id = int(_input("ID del álbum a editar: "))
                artista_id = _listar_artistas_select()
                if not artista_id:
                    pausar(); continue
                titulo = _input("Nuevo título: ").strip()
                if not v.validar_nombre(titulo):
                    print("❌ Título inválido."); pausar(); continue
                anio = _input("Año (opcional): ").strip()
                if anio and not v.validar_anio(anio):
                    print("❌ Año inválido."); pausar(); continue
                db.actualizar_album(alb_id, titulo, artista_id, v.normalizar_anio(anio))
                print("✅ Álbum actualizado.")
            except Exception as e:
                print(f"❌ Error: {e}")
            pausar()
        elif op == "4":
            try:
                alb_id = int(_input("ID del álbum a eliminar: "))
                db.eliminar_album(alb_id)
                print("✅ Álbum eliminado.")
            except Exception as e:
                print(f"❌ Error: {e}")
            pausar()
        elif op == "5":
            return
        else:
            print("Opción inválida.")

# ------------- MENÚ CANCIONES -------------
def _listar_albums_select() -> Optional[int]:
    rows = db.obtener_albums()
    if not rows:
        print("No hay álbums (opcional). Puedes dejarlo vacío.")
        return None
    for r in rows:
        print(f"[{r[0]}] {r[1]} — {r[2]} ({r[3] if r[3] else 's/f'})")
    sel = _input("ID de álbum (Enter para omitir): ").strip()
    if not sel:
        return None
    try:
        return int(sel)
    except Exception:
        print("Selección inválida.")
        return None

def menu_canciones():
    while True:
        print("\n🎼 Canciones")
        print(SEP)
        print("1. Agregar canción")
        print("2. Ver canciones")
        print("3. Editar canción")
        print("4. Eliminar canción")
        print("5. Regresar")
        op = _input("Opción: ").strip()
        if op == "1":
            artista_id = _listar_artistas_select()
            if not artista_id:
                pausar(); continue
            album_id = _listar_albums_select()  # opcional
            titulo = _input("Título: ").strip()
            if not v.validar_nombre(titulo):
                print("❌ Título inválido."); pausar(); continue
            gen = seleccionar_genero()
            dur = _input("Duración mm:ss (opcional): ").strip()
            if dur and not v.validar_duracion(dur):
                print("❌ Duración inválida."); pausar(); continue
            anio = _input("Año (opcional): ").strip()
            if anio and not v.validar_anio(anio):
                print("❌ Año inválido."); pausar(); continue
            try:
                db.crear_cancion(
                    titulo, artista_id, album_id, gen, dur if dur else None, v.normalizar_anio(anio)
                )
                print("✅ Canción agregada.")
            except Exception as e:
                print(f"❌ Error: {e}")
            pausar()
        elif op == "2":
            rows = db.obtener_canciones()
            if not rows:
                print("Sin canciones registradas.")
            else:
                print(SEP)
                for r in rows:
                    cid, titulo, artista, album, gen, dur, anio = r
                    print(f"[{cid}] {titulo} — {artista} | Álbum: {album or 'N/A'} | Género: {gen or 'N/A'} | Dur: {dur or 'N/A'} | Año: {anio or 's/f'}")
            pausar()
        elif op == "3":
            try:
                can_id = int(_input("ID de la canción a editar: "))
                artista_id = _listar_artistas_select()
                if not artista_id:
                    pausar(); continue
                album_id = _listar_albums_select()  # opcional
                titulo = _input("Nuevo título: ").strip()
                if not v.validar_nombre(titulo):
                    print("❌ Título inválido."); pausar(); continue
                gen = seleccionar_genero()
                dur = _input("Duración mm:ss (opcional): ").strip()
                if dur and not v.validar_duracion(dur):
                    print("❌ Duración inválida."); pausar(); continue
                anio = _input("Año (opcional): ").strip()
                if anio and not v.validar_anio(anio):
                    print("❌ Año inválido."); pausar(); continue
                db.actualizar_cancion(
                    can_id, titulo, artista_id, album_id, gen, dur if dur else None, v.normalizar_anio(anio)
                )
                print("✅ Canción actualizada.")
            except Exception as e:
                print(f"❌ Error: {e}")
            pausar()
        elif op == "4":
            try:
                can_id = int(_input("ID de la canción a eliminar: "))
                db.eliminar_cancion(can_id)
                print("✅ Canción eliminada.")
            except Exception as e:
                print(f"❌ Error: {e}")
            pausar()
        elif op == "5":
            return
        else:
            print("Opción inválida.")
