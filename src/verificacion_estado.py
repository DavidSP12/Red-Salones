import zmq
import sys
import time

def main(endpoint_central, endpoint_respaldo, endpoint_salud_central):
    contexto = zmq.Context()
    socket_central = contexto.socket(zmq.REQ)
    socket_central.connect(endpoint_central)
    socket_central.setsockopt(zmq.LINGER, 1000)

    socket_respaldo = contexto.socket(zmq.REQ)
    socket_respaldo.connect(endpoint_respaldo)
    socket_respaldo.setsockopt(zmq.LINGER, 1000)

    fallos = 0
    while True:
        try:
            socket_central.send_json({"ping": True})
            socket_central.recv_json(timeout=1000)
            fallos = 0
            print("Servidor Central está vivo")
        except zmq.error.Again:
            fallos += 1
            print(f"Ping al Servidor Central falló ({fallos}/3)")
            if fallos >= 3:
                print("Servidor Central caído. Activando respaldo.")
                socket_respaldo.send_json({"activar": True})
                socket_respaldo.recv_json()
                print("Servidor de Respaldo activado")
                break
        time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python verificacion_estado.py <endpoint_central> <endpoint_salud_respaldo> <endpoint_salud_central>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])