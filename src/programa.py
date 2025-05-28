import zmq
import json
import sys
import random
import os

def main(nombre, semestre, num_aulas, num_laboratorios, facultad, endpoint_facultad):
    contexto = zmq.Context()
    socket = contexto.socket(zmq.REQ)
    socket.connect(endpoint_facultad)

    # Generar solicitud
    solicitud = {
        "programa": nombre,
        "semestre": semestre,
        "aulas": int(num_aulas),
        "laboratorios": int(num_laboratorios),
        "facultad": facultad
    }

    # Enviar solicitud a la facultad
    socket.send_json(solicitud)
    print(f"Programa {nombre} envió solicitud: {solicitud}")

    # Recibir respuesta
    respuesta = socket.recv_json()
    print(f"Programa {nombre} recibió respuesta: {respuesta}")

    # Crear carpeta de salida si no existe
    os.makedirs("data", exist_ok=True)
    archivo = f"data/programa{nombre}_{semestre}.txt"
    with open(archivo, "a") as f:
        json.dump(respuesta, f)
        f.write("\n")

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Uso: python programa.py <nombre> <semestre> <num_aulas> <num_laboratorios> <facultad> <endpoint_facultad>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
