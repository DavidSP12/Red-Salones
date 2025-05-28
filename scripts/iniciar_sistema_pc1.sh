#!/bin/bash

echo "Liberando puerto 5566 y 5568 si están ocupados..."
fuser -k 5566/tcp
fuser -k 5568/tcp
fuser -k 5570/tcp

echo "Iniciando Servidor de Respaldo en PC1..."
python3 src/servidor_respaldo.py tcp://*:5556 2025-1 tcp://*:5570 &

sleep 2

echo "Iniciando Verificación de Estado en PC1..."
python3 src/verificacion_estado.py tcp://localhost:5555 tcp://localhost:5570 tcp://localhost:5557 &

echo "Iniciando Programas en PC1..."
python3 src/programa.py Química 2025-1 8 3 Ciencias tcp://10.43.96.13:6000 &
python3 src/programa.py Biología 2025-1 7 2 Ciencias tcp://10.43.96.13:6001 &
python3 src/programa.py Física 2025-1 7 2 Ciencias tcp://10.43.96.13:6002 &
python3 src/programa.py Geología 2025-1 6 2 Ciencias tcp://10.43.96.13:6003 &
python3 src/programa.py Astronomía 2025-1 7 3 Ciencias tcp://10.43.96.13:6004 &

echo "Componentes de PC1 iniciados."

