import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
# TÓPICOS ESPEJO PARA LA WEB
TOPIC_SUB = "clase/redes/equipo2/web_a_python"    # Recibe lo de la web
TOPIC_PUB = "clase/redes/equipo2/python_a_web"    # Envía a la web

def on_message(client, userdata, msg):
    print(f"\n[WEB]: {msg.payload.decode()}")
    print("Tú: ", end="", flush=True)

cliente = mqtt.Client()
cliente.on_message = on_message

try:
    cliente.connect(BROKER, PORT, 60)
    cliente.subscribe(TOPIC_SUB)
    cliente.loop_start()
    print("✅ Conectado. Sistema antiduplicados listo.")
    
    while True:
        msj = input("Tú: ")
        if msj.strip():
            cliente.publish(TOPIC_PUB, msj)
except KeyboardInterrupt:
    print("\nSaliendo...")
    cliente.disconnect()