import os
import time
import json
import matplotlib
matplotlib.use('Agg')  # Usa el backend 'Agg' para entornos sin GUI
import matplotlib.pyplot as plt
import inotify.adapters

def revisar_y_graficar():
    i = inotify.adapters.Inotify()
    i.add_watch('/shared_volume')  # Monitorear el volumen compartido

    for event in i.event_gen(yield_nones=False):
        (_, event_type, path, filename) = event
        if 'IN_CREATE' in event_type or 'IN_MODIFY' in event_type:
            if filename.endswith('.txt'):
                filepath = os.path.join(path, filename)
                print(f"Nuevo archivo detectado: {filepath}")
                try:
                    with open(filepath, 'r') as f:
                        data = f.readlines()
                        lista = json.loads(data[0].strip().split(":")[1])
                        suma = float(data[1].strip().split(":")[1])
                        promedio = float(data[2].strip().split(":")[1])
                        normalidad = data[3].strip().split(":")[1]

                        plt.figure()
                        plt.plot(lista, label=f'Suma: {suma}, Promedio: {promedio}')
                        plt.title(f"Distribución Normal: {normalidad}")
                        plt.xlabel('Indice')
                        plt.ylabel('Valor')
                        plt.legend()

                        # Guardar la grafica
                        output_path = filepath.replace('.txt', '.png')
                        plt.savefig(output_path)
                        plt.close()

                        print(f"Grafica guardada en {output_path}")

                        # Eliminar el archivo txt original
                        os.remove(filepath)
                        print(f"Archivo {filepath} eliminado tras generar la grafica.")

                except Exception as e:
                    print(f"Error al procesar el archivo {filepath}: {e}")
                time.sleep(1)

if __name__ == "__main__":
    revisar_y_graficar()
