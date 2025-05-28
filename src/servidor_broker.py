import zmq
import json
import threading
import sys
import time
from datetime import datetime

class ServidorCentral:
    def __init__(self, semestre):
        self.aulas_disponibles = 380
        self.laboratorios_disponibles = 60
        self.asignaciones = []
        self.no_atendidas = []
        self.lock = threading.Lock()
        self.semestre = semestre

    def asignar_recursos(self, facultad, programa, aulas, laboratorios):
        with self.lock:
            respuesta = {"facultad": facultad, "programa": programa, "asignado": {}, "estado": "exito"}
            aulas_asignadas = 0
            laboratorios_asignados = 0
            aulas_moviles = 0

            # Asignar laboratorios
            if laboratorios > 0:
                if self.laboratorios_disponibles >= laboratorios:
                    self.laboratorios_disponibles -= laboratorios
                    laboratorios_asignados = laboratorios
                else:
                    laboratorios_asignados = self.laboratorios_disponibles
                    self.laboratorios_disponibles = 0
                    laboratorios_restantes = laboratorios - laboratorios_asignados
                    if self.aulas_disponibles >= laboratorios_restantes:
                        self.aulas_disponibles -= laboratorios_restantes
                        aulas_moviles = laboratorios_restantes
                    else:
                        respuesta["estado"] = "fallo"
                        print(f"ALERTA: Laboratorios insuficientes para {facultad}/{programa}. Solicitados: {laboratorios}, Asignados: {laboratorios_asignados}, Móviles: {aulas_moviles}")

            # Asignar aulas
            if aulas > 0:
                if self.aulas_disponibles >= aulas:
                    self.aulas_disponibles -= aulas
                    aulas_asignadas = aulas
                else:
                    respuesta["estado"] = "fallo"
                    aulas_asignadas = self.aulas_disponibles
                    self.aulas_disponibles = 0
                    print(f"ALERTA: Aulas insuficientes para {facultad}/{programa}. Solicitadas: {aulas}, Asignadas: {aulas_asignadas}")

            respuesta["asignado"] = {
                "aulas": aulas_asignadas,
                "laboratorios": laboratorios_asignados,
                "aulas_moviles": aulas_moviles
            }

            self.asignaciones.append({
                "timestamp": datetime.now().isoformat(),
                "facultad": facultad,
                "programa": programa,
                "solicitud": {"aulas": aulas, "laboratorios": laboratorios},
                "respuesta": respuesta["asignado"],
                "estado": respuesta["estado"]
            })
            with open(f"asignaciones_{self.semestre}.txt", "a") as f:
                json.dump(self.asignaciones[-1], f)
                f.write("\n")

            if respuesta["estado"] == "fallo":
                self.no_atendidas.append({
                    "facultad": facultad,
                    "programa": programa,
                    "no_atendido": {
                        "aulas": aulas - aulas_asignadas,
                        "laboratorios": laboratorios - laboratorios_asignados - aulas_moviles
                    }
                })
                with open(f"no_atendidas_{self.semestre}.txt", "a") as f:
                    json.dump(self.no_atendidas[-1], f)
                    f.write("\n")

            return respuesta

def trabajador(contexto, servidor, endpoint_backend):
    socket = contexto.socket(zmq.REP)
    socket.connect(endpoint_backend)
    while True:
        solicitud = socket.recv_json()
        facultad = solicitud["facultad"]
        solicitud_programa = solicitud["solicitud_programa"]
        programa = solicitud_programa["programa"]
        aulas = solicitud_programa["aulas"]
        laboratorios = solicitud_programa["laboratorios"]

        print(f"Trabajador procesando solicitud de {facultad}/{programa}")
        respuesta = servidor.asignar_recursos(facultad, programa, aulas, laboratorios)
        socket.send_json(respuesta)

        confirmacion = socket.recv_json()
        print(f"Trabajador recibió confirmación de {facultad}: {confirmacion}")
        socket.send_json({"estado": "confirmado"})

def main(endpoint_frontend, endpoint_backend, semestre):
    servidor = ServidorCentral(semestre)
    contexto = zmq.Context()

    # Frontend: ROUTER para clientes
    frontend = contexto.socket(zmq.ROUTER)
    frontend.bind(endpoint_frontend)

    # Backend: DEALER para trabajadores
    backend = contexto.socket(zmq.DEALER)
    backend.bind(endpoint_backend)

    # Iniciar trabajadores
    for _ in range(5):  # 5 hilos trabajadores
        threading.Thread(target=trabajador, args=(contexto, servidor, endpoint_backend), daemon=True).start()

    # Iniciar proxy (balanceo de carga)
    print(f"Servidor Central (Broker) iniciado en {endpoint_frontend}")
    zmq.proxy(frontend, backend)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python servidor_broker.py <endpoint_frontend> <endpoint_backend> <semestre>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])