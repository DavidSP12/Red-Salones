# Informe de la Segunda Entrega: Sistema de Gestión de Aulas

## Resumen Actualizado del Sistema
El sistema completo ahora incluye:
- 50 procesos de programas generando solicitudes aleatorias (7–10 aulas, 2–4 laboratorios).
- 10 procesos de facultades retransmitiendo solicitudes/respuestas.
- Servidor central con dos implementaciones: cliente/servidor asíncrono y balanceo de carga.
- Servidor de respaldo con verificación de estado para tolerancia a fallos.
- Persistencia basada en archivos para todos los datos (asignaciones, solicitudes no atendidas, respuestas de programas).
- Despliegue en 3 máquinas según lo especificado.

## Detalles de la Arquitectura
- **Despliegue**: Ver diagrama de despliegue. Los programas se distribuyen en PC1, PC2, PC3; facultades en PC2; servidor central en PC3; servidor de respaldo y verificación de estado en PC1.
- **Patrones de Comunicación**:
  - Programa-Facultad: ZeroMQ REQ-REP (síncrono).
  - Facultad-Servidor: ZeroMQ REQ-REP asíncrono o ROUTER-DEALER (broker).
  - Verificación de Estado: Patrón de heartbeat de ZeroMQ.
- **Tolerancia a Fallos**: La verificación de estado detecta fallos del servidor central tras 3 pings fallidos, activa el servidor de respaldo, que sincroniza el estado desde archivos.
- **Persistencia**: Archivos basados en JSON para asignaciones, solicitudes no atendidas y respuestas de programas, asegurando durabilidad y legibilidad.

## Tecnologías Usadas
- **Python 3.8+**: Lenguaje principal para todos los componentes.
- **pyzmq**: Bindings de ZeroMQ para comunicación.
- **threading**: Concurrencia en el servidor para manejar múltiples solicitudes.
- **json**: Almacenamiento de datos estructurado.
- **time**: Medición de rendimiento.
- **os/sys**: Gestión de procesos y argumentos.

## Implementación de Tolerancia a Fallos
- **Verificación de Estado**: `verificacion_estado.py` envía pings cada segundo. En caso de fallo, señala a `servidor_respaldo.py` para que se vincule al endpoint del servidor central.
- **Servidor de Respaldo**: Sincroniza el estado leyendo `asignaciones_<semestre>.txt` y `no_atendidas_<semestre>.txt` antes de activarse.
- **Reconexión**: Los clientes de facultades usan el patrón de reconexión de ZeroMQ para cambiar al servidor de respaldo de forma transparente.

## Medición de Rendimiento
Ver informe de rendimiento para detalles. Las métricas se recolectaron usando el módulo `time` de Python, con timestamps registrados en puntos de solicitud y respuesta. Los resultados se analizaron con `pandas` y visualizaron con `matplotlib`.

## Guion del Video (10 Minutos)
1. **Introducción (1 min)**: Resumen del proyecto, objetivos y equipo.
2. **Arquitectura (2 min)**: Mostrar diagrama de despliegue, explicar distribución de componentes y patrones de comunicación.
3. **Demo (4 min)**:
   - Iniciar servidores, facultades y programas en 3 máquinas.
   - Mostrar solicitudes de programas, retransmisión de facultades y asignaciones del servidor en consola.
   - Simular fallo del servidor, demostrar activación del respaldo.
   - Mostrar archivos de registro (`asignaciones_2025-1.txt`, `programa_Psicología_2025-1.txt`).
4. **Rendimiento (2 min)**: Presentar métricas clave (tiempos de respuesta, tasas de éxito) con gráficos.
5. **Conclusión (1 min)**: Resumir logros, lecciones aprendidas y mejoras futuras.

## Configuración de Demo
- **Máquinas**: 3 máquinas virtuales (Ubuntu 20.04) con Python y pyzmq instalados.
- **Ejecución**:
  - PC1: Ejecutar `servidor_respaldo.py`, `verificacion_estado.py` y 20 instancias de programas.
  - PC2: Ejecutar 10 instancias de facultades y 20 instancias de programas.
  - PC3: Ejecutar `servidor_asincrono.py` o `servidor_broker.py` y 10 instancias de programas.
- **Verificación**: Revisar salidas en consola, archivos de registro y simular fallo del servidor durante el demo.