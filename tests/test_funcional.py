```python
import pytest
import json
import os
import subprocess
import time

# Prueba para verificar la persistencia de las respuestas del programa
def test_persistencia_programa():
    # Iniciar una facultad y el servidor para la prueba
    subprocess.Popen(["python", "src/servidor_asincrono.py", "tcp://*:5555", "2025-1"])
    time.sleep(2)
    subprocess.Popen(["python", "src/facultad.py", "Ciencias Sociales", "2025-1", "tcp://localhost:5555", "6000", "asincrono"])
    time.sleep(2)

    # Ejecutar un programa
    os.system("python src/programa.py Psicología 2025-1 7 2 tcp://localhost:6000")

    # Verificar que el archivo de salida existe y contiene datos correctos
    assert os.path.exists("data/programa_Psicología_2025-1.txt")
    with open("data/programa_Psicología_2025-1.txt", "r") as f:
        data = json.loads(f.readline())
        assert data["programa"] == "Psicología"
        assert data["estado"] == "exito"
        assert data["asignado"]["aulas"] == 7
        assert data["asignado"]["laboratorios"] == 2

# Prueba para verificar las asignaciones del servidor
def test_asignaciones_servidor():
    assert os.path.exists("data/asignaciones_2025-1.txt")
    with open("data/asignaciones_2025-1.txt", "r") as f:
        data = json.loads(f.readline())
        assert data["facultad"] == "Ciencias Sociales"
        assert data["programa"] == "Psicología"
        assert data["estado"] == "exito"
```