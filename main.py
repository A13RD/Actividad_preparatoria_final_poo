import json
from cifradorMensajes.modelo.cifrador import ReglaCifradoTraslacion, ReglaCifradoNumerico, Cifrador
from cifradorMensajes.modelo.errores import ErrorContenido, ErrorFormato


def procesar_mensaje(cifrador, mensaje, descripcion):
    print(f"\nProbando mensaje: '{mensaje}'")
    print(f"Descripción: {descripcion}")
    print(f"Usando cifrador: {cifrador.agente.__class__.__name__}")

    try:
        # Intentar encriptar
        mensaje_cifrado = cifrador.encriptar(mensaje)
        print(f"Mensaje cifrado: {mensaje_cifrado}")

        # Intentar desencriptar
        mensaje_descifrado = cifrador.desencriptar(mensaje_cifrado)
        print(f"Mensaje descifrado: {mensaje_descifrado}")
        print("✅ Mensaje procesado exitosamente")

    except (ErrorContenido, ErrorFormato) as e:
        print(f"❌ Error: {str(e)}")
    except Exception as e:
        print(f"❌ Múltiples errores: {str(e)}")


def main():
    # Crear los cifradores
    cifrador_numerico = Cifrador(ReglaCifradoNumerico(token=5))
    cifrador_traslacion = Cifrador(ReglaCifradoTraslacion(token=3))

    # Leer archivo de mensajes
    try:
        with open('mensajes_prueba.json', 'r', encoding='utf-8') as file:
            datos = json.load(file)
    except FileNotFoundError:
        print("Error: No se encontró el archivo mensajes_prueba.json")
        return
    except json.JSONDecodeError:
        print("Error: El archivo no tiene un formato JSON válido")
        return

    # Procesar cada mensaje
    print("=== Iniciando pruebas de cifrado ===")
    for caso in datos['mensajes']:
        mensaje = caso['texto']
        descripcion = caso['descripcion']

        print("\n=== Prueba con cifrado numérico ===")
        procesar_mensaje(cifrador_numerico, mensaje, descripcion)

        print("\n=== Prueba con cifrado por traslación ===")
        procesar_mensaje(cifrador_traslacion, mensaje, descripcion)

        print("\n" + "=" * 50)


if __name__ == "__main__":
    main()