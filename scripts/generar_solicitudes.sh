#!/bin/bash

# Script para generar solicitudes de prueba masivas
# Conecta a una facultad en PC2 (IP: 192.168.1.20)
# Uso: bash generar_solicitudes.sh [minima|maxima]

if [ "$1" == "minima" ]; then
    echo "Generando solicitudes de carga mínima (7 aulas, 2 laboratorios)..."
    for i in {1..25}; do
        python src/programa.py "Programa$i" 2025-1 7 2 tcp://192.168.1.20:6000 &
    done
elif [ "$1" == "maxima" ]; then
    echo "Generando solicitudes de carga máxima (10 aulas, 4 laboratorios)..."
    for i in {1..25}; do
        python src/programa.py "Programa$i" 2025-1 10 4 tcp://192.168.1.20:6000 &
    done
else
    echo "Uso: bash generar_solicitudes.sh [minima|maxima]"
    exit 1
fi

echo "Solicitudes generadas. Revisa data/metricas.csv para resultados."