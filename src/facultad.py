import zmq
import json
import threading
import sys

def manejar_programa(contexto, nombre_facultad, endpoint_programa, endpoint_servidor, semestre, patron):
    socket = contexto.socket(zmq.REP)
    socket.bind(endpoint_programa)

    # Recibir solicitud del programa
    solicitud = socket.recv_json()
    print(f"Facultad {nombre_facultad} recibió del programa: {solicitud}")

    # Reenviar al servidor
    socket_cliente = contexto.socket(zmq.REQ if patron == "asincrono" else zmq.DEALER)
    socket_cliente.connect(endpoint_servidor)
    solicitud_servidor = {
        "facultad": nombre_facultad,
        "semestre": semestre,
        "solicitud_programa": solicitud
    }
    socket_cliente.send_json(solicitud_servidor)

    # Recibir respuesta
    respuesta = socket_cliente.recv_json()
    print(f"Facultad {nombre_facultad} recibió del servidor: {respuesta}")

    # Enviar respuesta al programa
    socket.send_json(respuesta)

    # Confirmar asignación al servidor
    socket_cliente.send_json({"facultad": nombre_facultad, "confirmar": True})
    socket_cliente.recv_json()  # Confirmación de recepción

def main(nombre_facultad, semestre, endpoint_servidor, puerto_base_programa, patron):
    contexto = zmq.Context()
    hilos = []

    # Iniciar hilos para cada programa (5 programas)
    for i in range(5):
        endpoint_programa = f"tcp://*:{puerto_base_programa + i}"
        t = threading.Thread(target=manejar_programa, args=(contexto, nombre_facultad, endpoint_programa, endpoint_servidor, semestre, patron))
        t.start()
        hilos.append(t)

    for t in hilos:
        t.join()

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Uso: python facultad.py <nombre_facultad> <semestre> <endpoint_servidor> <puerto_base_programa> <patron>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5])