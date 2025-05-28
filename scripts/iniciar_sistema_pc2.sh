#!/bin/bash

# Script para iniciar componentes en PC2 (IP: 10.43.96.13)
# Solo 10 Facultades

echo "Liberando puertos 6000-6045 en PC2 (10.43.96.13)..."
# Terminar procesos que estén usando los puertos 6000, 6005, ..., 6045
for port in 6000 6005 6010 6015 6020 6025 6030 6035 6040 6045; do
    pid=$(lsof -t -i:$port)
    if [ -n "$pid" ]; then
        echo "Terminando proceso en puerto $port (PID: $pid)..."
        kill -9 $pid
    else
        echo "Puerto $port ya está libre."
    fi
done

# También terminamos cualquier proceso de facultad.py que pueda estar corriendo
echo "Terminando procesos previos de facultad.py..."
pkill -f "python3 src/facultad.py" || echo "No se encontraron procesos de facultad.py corriendo."

echo "Iniciando Facultades en PC2 (10.43.96.13)..."
python3 src/facultad.py "Ciencias Sociales" 2025-1 tcp://10.43.103.34:5555 6000 asincrono &
python3 src/facultad.py "Ingeniería" 2025-1 tcp://10.43.103.34:5555 6005 asincrono &
python3 src/facultad.py "Medicina" 2025-1 tcp://10.43.103.34:5555 6010 asincrono &
python3 src/facultad.py "Derecho" 2025-1 tcp://10.43.103.34:5555 6015 asincrono &
python3 src/facultad.py "Ciencias" 2025-1 tcp://10.43.103.34:5555 6020 asincrono &
python3 src/facultad.py "Artes" 2025-1 tcp://10.43.103.34:5555 6025 asincrono &
python3 src/facultad.py "Economía" 2025-1 tcp://10.43.103.34:5555 6030 asincrono &
python3 src/facultad.py "Educación" 2025-1 tcp://10.43.103.34:5555 6035 asincrono &
python3 src/facultad.py "Humanidades" 2025-1 tcp://10.43.103.34:5555 6040 asincrono &
python3 src/facultad.py "Teología" 2025-1 tcp://10.43.103.34:5555 6045 asincrono &
sleep 2

echo "Facultades de PC2 iniciadas."
