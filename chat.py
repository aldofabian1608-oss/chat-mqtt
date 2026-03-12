import paho.mqtt.client as mqtt
import time

# CONFIGURACIÓN DE CANALES SEPARADOS
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC_SUB = "clase/redes/equipo2/web"    # Escucha a la Web
TOPIC_PUB = "clase/redes/equipo2/python" # Le responde a la Web

def on_message(client, userdata, msg):
    print(f"\n[MENSAJE DE LA WEB]: {msg.payload.decode()}")
    print("Tú (Escribe mensaje): ", end="", flush=True)

cliente = mqtt.Client()
cliente.on_message = on_message

print("Conectando al Broker...")
try:
    cliente.connect(BROKER, PORT, 60)
    cliente.subscribe(TOPIC_SUB) # Solo se suscribe a lo que envía la web
    cliente.loop_start()
    print("✅ LISTO. Modo antiduplicados activo.")
    
    while True:
        msj = input("Tú (Escribe mensaje): ")
        if msj.strip():
            cliente.publish(TOPIC_PUB, msj) # Publica en el canal de respuesta
except KeyboardInterrupt:
    print("\nDesconectando...")
    cliente.disconnect()