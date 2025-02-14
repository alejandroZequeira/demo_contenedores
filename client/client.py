import socket
import json
import numpy as np

def enviar_lista(numeros):
    host = 'server'
    port = 12345
    fragment_size = 1000  # Tamaño del fragmento de datos a enviar

    try:
        # Intentar establecer la conexión
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        for i in range(0, len(numeros), fragment_size):
            fragment = numeros[i:i + fragment_size]

            # Intentar serializar los datos
            try:
                data = json.dumps(fragment)
            except TypeError as e:
                print(f"Error al serializar los datos: {e}")
                break

            # Enviar datos fragmentados
            client_socket.send(data.encode())
        
        print("Datos enviados exitosamente.")
    except (socket.error, ConnectionRefusedError) as e:
        print(f"Error de conexión: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        client_socket.close()

def generar_lista_aleatoria(tam):
    return np.random.randint(1, 100, tam).tolist()

def cliente():
    while True:
        comando = input("Ingrese comando (send <cantidad> o exit): ")
        
        if comando.startswith("send"):
            _, cantidad = comando.split()
            cantidad = int(cantidad)
            lista = generar_lista_aleatoria(cantidad)
            enviar_lista(lista)
        
        elif comando == "exit":
            print("Saliendo del cliente.")
            break

if __name__ == "__main__":
    cliente()
