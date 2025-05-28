# Sistema de Gestión de Aulas

## Resumen
Este proyecto implementa un sistema distribuido para gestionar la asignación de aulas y laboratorios en una universidad, según los requisitos del curso "Introducción a los Sistemas Distribuidos" de la Pontificia Universidad Javeriana (2025-10). Utiliza Python, ZeroMQ y hilos para manejar solicitudes concurrentes en 10 facultades, 50 programas académicos y un servidor central, con tolerancia a fallos mediante un servidor de respaldo.
Integrantes:
David Santiago Piñeros Rodriguez
Gabriel Alejandro Camacho Rivera
Santiago Avila Barbudo
## Requisitos
- Python 3.8+
- pyzmq (`pip install pyzmq`)
- 3 máquinas (físicas o virtuales) con conectividad de red
- Puertos TCP abiertos: 5555 (servidor central), 5556 (servidor respaldo), 5557 (verificación de estado), 6000–6050 (facultades/programas)

## Configuración
1. **Instalar Dependencias**:
   ```bash
   pip install pyzmq
   ```
2. **Configurar Máquinas**:
   - PC1: Programas académicos, servidor de respaldo (`servidor_respaldo.py`), verificación de estado (`verificacion_estado.py`).
   - PC2: Programas académicos, facultades (`facultad.py`).
   - PC3: Programas académicos, servidor central (`servidor_asincrono.py` o `servidor_broker.py`).
3. **Estructura de Directorios**:
   ```
   gestion_aulas/
   ├── programa.py
   ├── facultad.py
   ├── servidor_asincrono.py
   ├── servidor_broker.py
   ├── servidor_respaldo.py
   ├── verificacion_estado.py
   └── asignaciones_<semestre>.txt (generado)
   ```

## Ejecución del Sistema
1. **Iniciar el Servidor de Respaldo (PC1)**:
   ```bash
   python servidor_respaldo.py tcp://*:5555 2025-1 tcp://*:5557
   ```
2. **Iniciar el Proceso de Verificación de Estado (PC1)**:
   ```bash
   python verificacion_estado.py tcp://<IP_PC3>:5555 tcp://<IP_PC1>:5557 tcp://<IP_PC3>:5555
   ```
3. **Iniciar el Servidor Central (PC3)**:
   - Para el patrón asíncrono:
     ```bash
     python servidor_asincrono.py tcp://*:5555 2025-1
     ```
   - Para el patrón de balanceo de carga:
     ```bash
     python servidor_broker.py tcp://*:5555 tcp://*:5556 2025-1
     ```
4. **Iniciar Facultades (PC2)**:
   Para cada facultad (ej., Ciencias Sociales):
   ```bash
   python facultad.py "Ciencias Sociales" 2025-1 tcp://<IP_PC3>:5555 6000 asincrono
   ```
   Usar puertos 6000–6004 para programas, incrementar en 5 por cada facultad.
5. **Iniciar Programas (PC1, PC2, PC3)**:
   Para cada programa (ej., Psicología):
   ```bash
   python programa.py Psicología 2025-1 7 2 tcp://<IP_PC2>:6000
   ```
   Distribuir programas en las máquinas, asegurando el endpoint correcto de la facultad.

## Pruebas
- Simular solicitudes ejecutando múltiples instancias de programas con conteos aleatorios de aulas/laboratorios (7–10, 2–4).
- Probar tolerancia a fallos matando el proceso del servidor central; la verificación de estado debe activar el servidor de respaldo.
- Verificar archivos de salida (`asignaciones_2025-1.txt`, `no_atendidas_2025-1.txt`, `programa_<nombre>_2025-1.txt`) para persistencia.

## Notas
- El patrón asíncrono (`servidor_asincrono.py`) usa un socket REP con hilos para concurrencia.
- El patrón de balanceo de carga (`servidor_broker.py`) usa ROUTER-DEALER con un proxy para distribución.
- La tolerancia a fallos usa verificación de estado con heartbeats, sincronizando estado vía archivos.
- Las métricas de rendimiento se pueden recolectar usando el módulo `time` de Python (ver sección de informe de rendimiento).
