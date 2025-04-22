import redis
import json
import uuid
import sys

# Conexión a KeyDB (puerto por defecto: 6379)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Prefijo para las claves
KEY_PREFIX = "libro:"


# Funciones
def agregar_libro():
    titulo = input("Título: ")
    autor = input("Autor: ")
    genero = input("Género: ")
    estado = input("Estado de lectura (leído/no leído): ").strip().lower()

    if estado not in ["leído", "no leído"]:
        print("Estado inválido.")
        return

    libro_id = str(uuid.uuid4())
    libro = {
        "id": libro_id,
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "estado_lectura": estado
    }

    r.set(KEY_PREFIX + libro_id, json.dumps(libro))
    print("Libro agregado correctamente.")


def ver_libros():
    claves = r.keys(KEY_PREFIX + "*")
    if not claves:
        print("No hay libros registrados.")
        return

    print("\nListado de libros:")
    for clave in claves:
        libro = json.loads(r.get(clave))
        print(f"[{libro['id']}] {libro['titulo']} - {libro['autor']} | {libro['genero']} | {libro['estado_lectura']}")


def actualizar_libro():
    ver_libros()
    libro_id = input("ID del libro a actualizar: ").strip()
    clave = KEY_PREFIX + libro_id

    if not r.exists(clave):
        print("Libro no encontrado.")
        return

    libro = json.loads(r.get(clave))

    print("¿Qué deseas actualizar?")
    print("1. Título\n2. Autor\n3. Género\n4. Estado de lectura")
    opcion = input("Opción: ")

    if opcion == "1":
        libro['titulo'] = input("Nuevo título: ")
    elif opcion == "2":
        libro['autor'] = input("Nuevo autor: ")
    elif opcion == "3":
        libro['genero'] = input("Nuevo género: ")
    elif opcion == "4":
        nuevo_estado = input("Nuevo estado (leído/no leído): ").strip().lower()
        if nuevo_estado in ["leído", "no leído"]:
            libro['estado_lectura'] = nuevo_estado
        else:
            print("Estado inválido.")
            return
    else:
        print("Opción inválida.")
        return

    r.set(clave, json.dumps(libro))
    print("Libro actualizado.")


def eliminar_libro():
    ver_libros()
    libro_id = input("ID del libro a eliminar: ").strip()
    clave = KEY_PREFIX + libro_id

    if r.delete(clave):
        print("Libro eliminado.")
    else:
        print("Libro no encontrado.")


def buscar_libros():
    print("Buscar por: 1. Título  2. Autor  3. Género")
    opcion = input("Opción: ")
    campo = None

    if opcion == "1":
        campo = "titulo"
    elif opcion == "2":
        campo = "autor"
    elif opcion == "3":
        campo = "genero"
    else:
        print("Opción inválida.")
        return

    valor = input("Buscar: ").lower()
    encontrados = False

    for clave in r.keys(KEY_PREFIX + "*"):
        libro = json.loads(r.get(clave))
        if valor in libro[campo].lower():
            encontrados = True
            print(
                f"[{libro['id']}] {libro['titulo']} - {libro['autor']} | {libro['genero']} | {libro['estado_lectura']}")

    if not encontrados:
        print("No se encontraron coincidencias.")


# Menú principal
def menu():
    while True:
        print("\n--- Menú Biblioteca Personal ---")
        print("1. Agregar nuevo libro")
        print("2. Actualizar información de un libro")
        print("3. Eliminar libro existente")
        print("4. Ver listado de libros")
        print("5. Buscar libros")
        print("6. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            agregar_libro()
        elif opcion == "2":
            actualizar_libro()
        elif opcion == "3":
            eliminar_libro()
        elif opcion == "4":
            ver_libros()
        elif opcion == "5":
            buscar_libros()
        elif opcion == "6":
            print("Programa terminado.")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nPrograma terminado.")
        sys.exit(0)
