import database as db
from interfaz import menu_principal, menu_artistas, menu_albums, menu_canciones

def main():
    db.crear_tablas()
    while True:
        opcion = menu_principal()
        if opcion == "1":
            menu_artistas()
        elif opcion == "2":
            menu_albums()
        elif opcion == "3":
            menu_canciones()
        elif opcion == "4":
            print("Saliendo... 👋")
            break
        else:
            print("❌ Opción inválida.")

if __name__ == "__main__":
    main()
