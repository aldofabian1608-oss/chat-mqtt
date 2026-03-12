import paho.mqtt.client as mqtt
import time

BROKER = "broker.hivemq.com"
TOPIC = "clase/redes/equipo2" # MISMO TÓPICO QUE EL HTML

def on_message(client, userdata, msg):
    print(f"\n[MENSAJE RECIBIDO]: {msg.payload.decode()}")
    print("Tú: ", end="", flush=True)

cliente = mqtt.Client()
cliente.on_message = on_message

print("Conectando...")
cliente.connect(BROKER, 1883)
cliente.subscribe(TOPIC)
cliente.loop_start()

print("✅ Chat activo. Escribe algo o 'salir' para terminar.")
try:
    while True:
        msj = input("Tú: ")
        if msj.lower() == 'salir': break
        cliente.publish(TOPIC, msj)
except KeyboardInterrupt:
    pass

cliente.loop_stop()
cliente.disconnect()