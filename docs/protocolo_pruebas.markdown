# Protocolo de Pruebas

## Pruebas Funcionales
1. **Generación de Solicitudes de Programas**:
   - **Entrada**: Ejecutar `programa.py` con aulas (7–10) y laboratorios (2–4) aleatorios.
   - **Esperado**: Solicitud enviada a la facultad, registrada en consola, almacenada en `programa_<nombre>_<semestre>.txt`.
2. **Retransmisión de Solicitudes por Facultades**:
   - **Entrada**: Facultad recibe 5 solicitudes de programas.
   - **Esperado**: Solicitudes reenviadas al servidor, respuestas retransmitidas, confirmadas con el servidor.
3. **Asignación de Recursos del Servidor**:
   - **Entrada**: Servidor recibe solicitudes de 350–500 aulas/laboratorios.
   - **Esperado**: Asigna recursos, adapta aulas móviles si los laboratorios se agotan, registra asignaciones y solicitudes no atendidas.
4. **Persistencia**:
   - **Entrada**: Ejecutar sistema con múltiples solicitudes.
   - **Esperado**: Archivos `asignaciones_<semestre>.txt`, `no_atendidas_<semestre>.txt` y registros de programas contienen datos JSON correctos.

## Pruebas de Fallos
1. **Fallo del Servidor**:
   - **Entrada**: Matar el proceso del servidor central durante operación.
   - **Esperado**: La verificación de estado detecta el fallo tras 3 pings fallidos, activa el servidor de respaldo, las facultades se reconectan, las operaciones continúan.
2. **Desconexión de Red**:
   - **Entrada**: Bloquear temporalmente la red al servidor central.
   - **Esperado**: Las facultades reintentan conexiones, reanudan una vez restaurada la red.

## Pruebas de Rendimiento
1. **Carga Mínima**:
   - **Entrada**: 5 facultades, 25 programas, 7 aulas, 2 laboratorios cada uno.
   - **Esperado**: Medir tiempos de respuesta, tasas de éxito/fallo, registrar en CSV.
2. **Carga Máxima**:
   - **Entrada**: 5 facultades, 25 programas, 10 aulas, 4 laboratorios cada uno.
   - **Esperado**: Mismas métricas, esperar mayor tasa de fallo debido a límites de recursos.

## Herramientas
- **pytest**: Automatizar pruebas funcionales.
- **Python time**: Medir métricas de rendimiento.
- **tcpdump**: Monitorear comunicación de red (opcional).

## Procedimiento
- Ejecutar pruebas automatizadas con `pytest` para verificación funcional.
- Realizar pruebas de rendimiento con ejecuciones de programas scripted, registrando métricas.
- Simular fallos manualmente durante el demo para mostrar resiliencia.