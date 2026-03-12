import paho.mqtt.client as mqtt
import time

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "clase/redes/equipo/final" # DEBE SER IGUAL AL DEL HTML

def on_message(client, userdata, msg):
    print(f"\n[MENSAJE DE LA WEB]: {msg.payload.decode()}")
    print("Tú: ", end="", flush=True)

cliente = mqtt.Client()
cliente.on_message = on_message

print("Conectando al servidor de mensajes...")
try:
    cliente.connect(BROKER, PORT, 60)
    cliente.subscribe(TOPIC)
    cliente.loop_start()
    print("✅ LISTO. Escribe algo para mandarlo a GitHub Pages.")
    
    while True:
        msj = input("Tú: ")
        cliente.publish(TOPIC, msj)
except KeyboardInterrupt:
    print("\nCerrando...")
    cliente.disconnect()