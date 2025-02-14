import socket
import json
import os
from datetime import datetime
from scipy.stats import shapiro

# Función para verificar si una lista tiene distribución normal usando la prueba de Shapiro-Wilk
def es_distribucion_normal(lista):
    from scipy.stats import shapiro
    stat, p_value = shapiro(lista)
    return p_value > 0.05  # Si p_value > 0.05, entonces los datos siguen una distribución normal

# Procesa la lista de números y determina si sigue una distribución normal
def procesar_lista_numeros(lista):
    suma = sum(lista)
    promedio = suma / len(lista)
    normalidad = es_distribucion_normal(lista)
    return suma, promedio, normalidad

def servidor():
    host = '0.0.0.0'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Servidor esperando conexión...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Conexión establecida con {addr}")

        lista_completa = []
        
        try:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                try:
                    fragmento = json.loads(data)
                    lista_completa.extend(fragmento)  # Reconstruir la lista a partir de los fragmentos
                except json.JSONDecodeError as e:
                    print(f"Error al decodificar JSON: {e}")
                    break  # Salir si hay error al decodificar

            if lista_completa:
                suma, promedio, normalidad = procesar_lista_numeros(lista_completa)
                print(f"Lista recibida: {lista_completa}")
                print(f"Suma: {suma}, Promedio: {promedio}, Normalidad: {normalidad}")

                # Guardar los resultados en un archivo
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"/shared_volume/resultado_{timestamp}.txt"
                with open(filename, "w") as f:
                    f.write(f"Lista: {lista_completa}\n")
                    f.write(f"Suma: {suma}\n")
                    f.write(f"Promedio: {promedio}\n")
                    f.write(f"Normalidad: {normalidad}\n")
        except socket.error as e:
            print(f"Error de conexión: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    servidor()
