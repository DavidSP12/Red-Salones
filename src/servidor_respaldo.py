import zmq
import json
import threading
import sys
import time
from datetime import datetime

class ServidorRespaldo:
    def __init__(self, semestre, endpoint_primario):
        self.aulas_disponibles = 380
        self.laboratorios_disponibles = 60
        self.asignaciones = []
        self.no_atendidas = []
        self.lock = threading.Lock()
        self.semestre = semestre
        self.endpoint_primario = endpoint_primario
        self.activo = False

    def sincronizar_estado(self):
        # Simular sincronización de estado leyendo archivos del servidor primario
        try:
            with open(f"asignaciones_{self.semestre}.txt", "r") as f:
                for linea in f:
                    asignacion = json.loads(linea.strip())
                    self.asignaciones.append(asignacion)
                    if asignacion["estado"] == "exito":
                        self.aulas_disponibles -= asignacion["respuesta"]["aulas"]
                        self.laboratorios_disponibles -= asignacion["respuesta"]["laboratorios"]
                        self.aulas_disponibles -= asignacion["respuesta"]["aulas_moviles"]
        except FileNotFoundError:
            pass

    def asignar_recursos(self, facultad, programa, aulas, laboratorios):
        with self.lock:
            respuesta = {"facultad": facultad, "programa": programa, "asignado": {}, "estado": "exito"}
            aulas_asignadas = 0
            laboratorios_asignados = 0
            aulas_moviles = 0

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

    def manejar_solicitud(self, socket, solicitud):
        facultad = solicitud["facultad"]
        solicitud_programa = solicitud["solicitud_programa"]
        programa = solicitud_programa["programa"]
        aulas = solicitud_programa["aulas"]
        laboratorios = solicitud_programa["laboratorios"]

        print(f"Servidor de Respaldo procesando solicitud de {facultad}/{programa}")
        respuesta = self.asignar_recursos(facultad, programa, aulas, laboratorios)
        socket.send_json(respuesta)

        confirmacion = socket.recv_json()
        print(f"Servidor de Respaldo recibió confirmación de {facultad}: {confirmacion}")
        socket.send_json({"estado": "confirmado"})

def main(endpoint, semestre, endpoint_salud):
    servidor = ServidorRespaldo(semestre, endpoint)
    contexto = zmq.Context()
    socket_salud = contexto.socket(zmq.REP)
    socket_salud.bind(endpoint_salud)

    while True:
        # Esperar señal de activación
        mensaje = socket_salud.recv_json()
        if mensaje.get("activar", False):
            servidor.activo = True
            servidor.sincronizar_estado()
            print("Servidor de Respaldo activado")
            socket_salud.send_json({"estado": "activo"})

            # Iniciar servicio de solicitudes
            socket = contexto.socket(zmq.REP)
            socket.bind(endpoint)
            while servidor.activo:
                solicitud = socket.recv_json()
                threading.Thread(target=servidor.manejar_solicitud, args=(socket, solicitud)).start()
        else:
            socket_salud.send_json({"estado": "en_espera"})

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python servidor_respaldo.py <endpoint> <semestre> <endpoint_salud>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])