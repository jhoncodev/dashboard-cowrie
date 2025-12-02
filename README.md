# Cowrie Honeypot Dashboard

Dashboard de monitoreo en tiempo real para el honeypot SSH Cowrie. Recibe eventos JSON y los visualiza con estadísticas y alertas en vivo.

## Autores

**Grupo 3 - Sistemas Operativos**

## Descripción

Este proyecto proporciona un dashboard web para monitorear ataques capturados por Cowrie, un honeypot SSH/Telnet de baja interacción. El sistema recibe eventos en formato JSON a través de un socket TCP y los muestra en tiempo real mediante WebSockets.

## Características

- **Monitoreo en tiempo real** - Visualización instantánea de eventos de ataque
- **Estadísticas en vivo** - Contador de ataques totales, intrusiones exitosas e IPs únicas
- **Alertas visuales y sonoras** - Notificaciones cuando ocurre una intrusión exitosa
- **Clasificación de eventos** - Diferenciación por colores según el tipo de evento:
  - 🔴 Intentos de login fallidos
  - 🟢 Intrusiones exitosas
  - 🟡 Comandos ejecutados
- **Interfaz oscura** - Diseño optimizado para centros de operaciones de seguridad

## Arquitectura

```
┌─────────────┐     JSON/TCP     ┌──────────────┐    WebSocket    ┌─────────────┐
│   Cowrie    │ ───────────────► │  dashboard.py │ ──────────────► │  Navegador  │
│  Honeypot   │     Puerto 5001  │    Flask      │    Puerto 5000  │    Web      │
└─────────────┘                  └──────────────┘                  └─────────────┘
```

## Requisitos

- Python 3.7+
- Cowrie Honeypot (configurado para enviar logs JSON)

## Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd Cowrie
   ```

2. **Instalar dependencias**
   ```bash
   pip install flask flask-socketio
   ```

3. **Configurar Cowrie** (opcional)

   Asegurarse de que Cowrie envíe los eventos JSON al puerto 5001 del servidor donde corre el dashboard.

## Uso

1. **Iniciar el dashboard**
   ```bash
   python dashboard.py
   ```

2. **Acceder al dashboard**

   Abrir el navegador en: `http://localhost:5000`

3. **Conectar Cowrie**

   Configurar Cowrie para enviar logs JSON a `<IP_DEL_DASHBOARD>:5001`

## Estructura del Proyecto

```
Cowrie/
├── dashboard.py        # Servidor Flask + listener TCP
├── templates/
│   └── index.html      # Interfaz web del dashboard
└── README.md           # Este archivo
```

## Configuración

Los parámetros se pueden modificar en `dashboard.py`:

| Variable | Valor por defecto | Descripción |
|----------|-------------------|-------------|
| `TCP_PORT` | 5001 | Puerto para recibir JSON de Cowrie |
| `WEB_PORT` | 5000 | Puerto del servidor web |
| `TCP_IP` | 0.0.0.0 | Interfaz de escucha TCP |

## Eventos Soportados

| Evento | Descripción |
|--------|-------------|
| `cowrie.login.failed` | Intento de login fallido |
| `cowrie.login.success` | Intrusión exitosa |
| `cowrie.command.input` | Comando ejecutado por atacante |

## Tecnologías Utilizadas

- **Backend**: Python, Flask, Flask-SocketIO
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Comunicación**: TCP Sockets, WebSockets

## Capturas de Pantalla

El dashboard muestra:
- Panel de estadísticas con contadores en tiempo real
- Tabla de eventos con scroll automático
- Indicador de estado de conexión
- Alertas visuales para eventos críticos

## Licencia

Proyecto académico Grupo 3 - Sistemas Operativos

---

*Laboratorio de Ciberseguridad - Proyecto Académico*
