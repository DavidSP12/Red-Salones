#!/bin/bash

# Script para iniciar componentes en PC3 (IP: 10.43.103.34)
# Servidor Central, 10 Programas
echo "Liberando puerto 6040 - 6049 si están ocupados..."
fuser -k 6040/tcp
fuser -k 6041/tcp
fuser -k 6042/tcp
fuser -k 6043/tcp
fuser -k 6044/tcp
fuser -k 6045/tcp
fuser -k 6046/tcp
fuser -k 6047/tcp
fuser -k 6048/tcp
fuser -k 6049/tcp

echo "Iniciando Servidor Central en PC3..."
python3 src/servidor_asincrono.py tcp://*:5555 2025-1 &
sleep 2

echo "Iniciando Programas en PC3..."

# 10 programas, conectando a facultades en PC2 (10.43.96.13)
python3 src/programa.py Literatura 2025-1 7 2 Humanidades tcp://10.43.96.13:6040 &
python3 src/programa.py Filosofía 2025-1 8 3 Humanidades tcp://10.43.96.13:6041 &
python3 src/programa.py Lingüística 2025-1 7 2 Humanidades tcp://10.43.96.13:6042 &
python3 src/programa.py Arqueología 2025-1 8 3 Humanidades tcp://10.43.96.13:6043 &
python3 src/programa.py Sociología_Humanidades 2025-1 7 2 Humanidades tcp://10.43.96.13:6044 &
python3 src/programa.py Ética 2025-1 7 2 Humanidades tcp://10.43.96.13:6045 &
python3 src/programa.py Metafísica 2025-1 8 3 Humanidades tcp://10.43.96.13:6046 &
python3 src/programa.py Teología_Bíblica 2025-1 7 2 Teología tcp://10.43.96.13:6047 &
python3 src/programa.py Pastoral 2025-1 8 3 Teología tcp://10.43.96.13:6048 &
python3 src/programa.py Filosofía_Religiosa 2025-1 7 2 Teología tcp://10.43.96.13:6049 &

echo "Componentes de PC3 iniciados."
#a
