import socket
import json
import threading
from flask import Flask, render_template
from flask_socketio import SocketIO

TCP_IP = '0.0.0.0'
TCP_PORT = 5001
WEB_PORT = 5000

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secreto'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

stats = { "intentos": 0, "intrusiones": 0, "ips_unicas": set() }

def parse_and_emit(json_str):
    """Parsea el JSON y lo envía a la web si es válido"""
    try:
        if not json_str.strip(): return
        
        log = json.loads(json_str)
        eventid = log.get('eventid', '')
        
        if "cowrie.session" in eventid or "cowrie.client" in eventid:
            return

        timestamp = log.get('timestamp', '')[11:19]
        src_ip = log.get('src_ip', 'Desconocida')
        stats['ips_unicas'].add(src_ip)
        
        data = { "time": timestamp, "ip": src_ip, "type": "", "msg": "", "color": "info" }

        if "cowrie.login.failed" in eventid:
            stats['intentos'] += 1
            data['type'] = "LOGIN FALLIDO"
            data['msg'] = f"User: {log.get('username')} | Pass: {log.get('password')}"
            data['color'] = "danger"
        elif "cowrie.login.success" in eventid:
            stats['intrusiones'] += 1
            data['type'] = "INTRUSIÓN"
            data['msg'] = f"User: {log.get('username')} | Pass: {log.get('password')}"
            data['color'] = "success"
        elif "cowrie.command.input" in eventid:
            data['type'] = "COMANDO"
            data['msg'] = log.get('input')
            data['color'] = "warning"
        else:
            data['type'] = eventid.split('.')[-1]
            data['msg'] = "Evento registrado"

        data['stats'] = {
            "total": stats['intentos'] + stats['intrusiones'],
            "hacked": stats['intrusiones'],
            "unique_ips": len(stats['ips_unicas'])
        }
        
        print(f"ENVIANDO A WEB: {data['type']} desde {data['ip']}")
        socketio.emit('new_log', data)

    except json.JSONDecodeError:
        print(f"Error decodificando JSON: {json_str[:20]}...")
    except Exception as e:
        print(f"Error procesando: {e}")

def tcp_listener():
    """Escucha datos crudos de Netcat"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((TCP_IP, TCP_PORT))
            s.listen()
            print(f"--- TCP LISTENER ESPERANDO EN PUERTO {TCP_PORT} ---")
        except Exception as e:
            print(f"ERROR AL ABRIR PUERTO {TCP_PORT}: {e}")
            print("¿Quizás otro script sigue corriendo? Cierra todas las terminales.")
            return

        while True:
            print("Esperando conexión de Ubuntu...")
            conn, addr = s.accept()
            print(f"CONECTADO CON UBUNTU: {addr}")
            with conn:
                buffer = ""
                while True:
                    try:
                        data = conn.recv(1024)
                        if not data: break
                        
                        part = data.decode('utf-8', errors='ignore')
                        buffer += part
                        
                        while '\n' in buffer:
                            line, buffer = buffer.split('\n', 1)
                            parse_and_emit(line)
                            
                    except Exception as e:
                        print(f"Error en recepción: {e}")
                        break
            print("Desconectado. Esperando reconexión...")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    t = threading.Thread(target=tcp_listener)
    t.daemon = True
    t.start()
    
    print(f"--- WEB: http://localhost:{WEB_PORT} ---")
    socketio.run(app, host='0.0.0.0', port=WEB_PORT, debug=False, allow_unsafe_werkzeug=True)