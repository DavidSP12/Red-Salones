# Informe de la Primera Entrega: Sistema de Gestión de Aulas

## Modelos del Sistema
### Modelo Arquitectónico
El sistema sigue una arquitectura cliente-servidor con un servidor central (DTI) que maneja la asignación de recursos, 10 procesos de facultades como intermediarios y 50 procesos de programas como clientes. El servidor usa hilos para concurrencia, y ZeroMQ asegura comunicación confiable. Un servidor de respaldo y un proceso de verificación de estado proporcionan tolerancia a fallos.

### Modelo de Interacción
- **Programa-Facultad**: Request-reply síncrono (ZeroMQ REQ-REP) para enviar solicitudes y recibir respuestas.
- **Facultad-Servidor**: Cliente/servidor asíncrono (ZeroMQ REQ-REP con hilos) para esta entrega, con balanceo de carga planeado para la segunda entrega.
- **Verificación de Estado**: Patrón de heartbeat para monitorear el estado del servidor.

### Modelo de Fallos
- **Fallo del Servidor**: Manejado por un servidor de respaldo que se activa en caso de fallo, detectado mediante verificación de estado.
- **Problemas de Red**: El patrón de reconexión de ZeroMQ asegura comunicación robusta.
- **Consistencia de Datos**: Bloqueos de hilos previenen condiciones de carrera durante la asignación de recursos.

### Modelo de Seguridad
- **Control de Acceso**: Solo programas/facultades autorizados se comunican con el servidor vía endpoints predefinidos.
- **Integridad de Datos**: Persistencia basada en archivos asegura almacenamiento consistente de asignaciones y solicitudes no atendidas.
- **Sin Autenticación**: Se asume un entorno confiable por simplicidad (futuro trabajo podría añadir autenticación).

## Diseño del Sistema
### Diagrama de Despliegue
Ver sección de arquitectura (descrita arriba). Los componentes se distribuyen en 3 máquinas, con conexiones TCP para comunicación.

### Diagrama de Componentes
- **Programa**: Genera y envía solicitudes, registra respuestas.
- **Facultad**: Retransmite solicitudes/respuestas entre programas y servidor.
- **Servidor**: Asigna recursos, registra asignaciones, maneja concurrencia.
- **Servidor de Respaldo**: En espera para conmutación.
- **Verificación de Estado**: Monitorea el estado del servidor.

### Diagrama de Clases
Ver sección de arquitectura. Clases clave incluyen Programa, Facultad, ServidorCentral, ServidorRespaldo y VerificacionEstado, con herencia para ServidorRespaldo.

### Diagrama de Secuencia
Describe el flujo desde la solicitud del programa hasta la asignación del servidor, incluyendo hilos y pasos de confirmación.

## Protocolo de Pruebas
### Pruebas Funcionales
- **Solicitud de Programa**: Verificar que los programas envíen solicitudes correctas (7–10 aulas, 2–4 laboratorios) y almacenen respuestas.
- **Retransmisión de Facultad**: Asegurar que las facultades reenvíen solicitudes y confirmen asignaciones.
- **Asignación del Servidor**: Probar asignación de recursos, adaptación de aulas móviles y generación de alertas para solicitudes no cumplidas.
- **Persistencia**: Verificar que los archivos (`asignaciones_<semestre>.txt`, `programa_<nombre>_<semestre>.txt`) contengan datos correctos.

### Pruebas de Fallos
- **Fallo del Servidor**: Simular fallo del servidor central y verificar activación del respaldo (segunda entrega).
- **Desconexión de Red**: Probar lógica de reconexión de ZeroMQ.

### Pruebas de Rendimiento
- Medir tiempos de respuesta y tasas de éxito para 5 facultades (25 programas) con solicitudes mínimas/máximas (ver sección de rendimiento).

## Metodología para Métricas de Rendimiento
- **Herramientas**: Módulo `time` de Python para medir tiempos de solicitudes y respuestas.
- **Instrumentación**:
  - Añadir timestamps en `facultad.py` y `servidor_asincrono.py` para medir:
    - Tiempo desde la solicitud del programa hasta la respuesta de la facultad.
    - Tiempo desde la solicitud de la facultad hasta la respuesta del servidor.
  - Contar asignaciones exitosas/fallidas en los registros del servidor.
- **Procedimiento**:
  - Ejecutar 5 facultades con 5 programas cada una, probando escenarios mínimo (7 aulas, 2 laboratorios) y máximo (10 aulas, 4 laboratorios).
  - Registrar tiempos y conteos en CSV para análisis.
- **Herramientas Consideradas**: `pytest` para pruebas automatizadas, `pandas` para análisis de datos, `matplotlib` para graficar.

## Estado de la Implementación
- **Implementado**:
  - Procesos de facultades enviando solicitudes al servidor (`facultad.py`).
  - Servidor concurrente manejando solicitudes con hilos (`servidor_asincrono.py`).
  - Asignación de recursos con adaptación de aulas móviles.
  - Persistencia basada en archivos para asignaciones.
- **Pendiente** (para la segunda entrega):
  - Procesos de programas.
  - Patrón de balanceo de carga.
  - Tolerancia a fallos con servidor de respaldo y verificación de estado.
- **Configuración de Demo**: Funciona en 2 máquinas (PC2: facultades, PC3: servidor). Los programas se simularán manualmente para esta entrega.