```python
import pytest
import os
import time
import pandas as pd

# Prueba de rendimiento para carga mínima
def test_rendimiento_carga_minima():
    # Iniciar el sistema
    os.system("bash scripts/iniciar_sistema.sh")
    time.sleep(5)  # Esperar a que el sistema esté listo

    # Generar solicitudes de carga mínima
    start_time = time.time()
    os.system("bash scripts/generar_solicitudes.sh minima")
    time.sleep(10)  # Esperar a que se procesen las solicitudes

    # Verificar métricas
    assert os.path.exists("data/metricas.csv")
    df = pd.read_csv("data/metricas.csv")
    assert df["tiempo_extremo_a_extremo"].mean() < 200  # Umbral en ms
    assert df["estado"].value_counts()["exito"] / len(df) > 0.9  # >90% éxito

# Prueba de rendimiento para carga máxima
def test_rendimiento_carga_maxima():
    # Iniciar el sistema
    os.system("bash scripts/iniciar_sistema.sh")
    time.sleep(5)

    # Generar solicitudes de carga máxima
    start_time = time.time()
    os.system("bash scripts/generar_solicitudes.sh maxima")
    time.sleep(10)

    # Verificar métricas
    assert os.path.exists("data/metricas.csv")
    df = pd.read_csv("data/metricas.csv")
    assert df["tiempo_extremo_a_extremo"].mean() < 250  # Umbral en ms
    assert df["estado"].value_counts()["exito"] / len(df) > 0.8  # >80% éxito
```