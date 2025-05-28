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
                    # Adaptar aulas como móviles
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

            # Registrar asignación
            self.asignaciones.append({
                "timestamp": datetime.now().isoformat(),
                "facultad": facultad,
                "programa": programa,
                "solicitud": {"aulas": aulas, "laboratorios": laboratorios},
                "respuesta": respuesta["asignado"],
                "estado": respuesta["estado"]
            })
            with open(f"data/asignaciones_{self.semestre}.txt", "a") as f:
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

    def manejar_solicitud(self, socket, solicitud):
        facultad = solicitud["facultad"]
        solicitud_programa = solicitud["solicitud_programa"]
        programa = solicitud_programa["programa"]
        aulas = solicitud_programa["aulas"]
        laboratorios = solicitud_programa["laboratorios"]

        print(f"Procesando solicitud de {facultad}/{programa}: {aulas} aulas, {laboratorios} laboratorios")
        respuesta = self.asignar_recursos(facultad, programa, aulas, laboratorios)
        socket.send_json(respuesta)

        # Esperar confirmación
        confirmacion = socket.recv_json()
        print(f"Recibida confirmación de {facultad}: {confirmacion}")

        # Confirmar recepción
        socket.send_json({"estado": "confirmado"})

def main(endpoint, semestre):
    servidor = ServidorCentral(semestre)
    contexto = zmq.Context()
    socket = contexto.socket(zmq.REP)
    socket.bind(endpoint)

    print(f"Servidor Central (Asíncrono) iniciado en {endpoint}")
    while True:
        solicitud = socket.recv_json()
        threading.Thread(target=servidor.manejar_solicitud, args=(socket, solicitud)).start()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python servidor_asincrono.py <endpoint> <semestre>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
