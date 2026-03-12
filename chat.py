import paho.mqtt.client as mqtt
import base64
import json
import io
from PIL import Image

BROKER = "broker.hivemq.com"
TOPIC = "clase/redes/equipo2/whatsapp_final_v3"
MI_ID = "Python_Aldo"

def procesar_imagen(ruta, es_perfil=False):
    with Image.open(ruta) as img:
        # Redimensionar drásticamente para que no tape el chat
        size = (80, 80) if es_perfil else (300, 300)
        img.thumbnail(size)
        
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        buffer = io.BytesIO()
        # Calidad baja (40-60) para que el Base64 sea corto
        img.save(buffer, format="JPEG", quality=50)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/jpeg;base64,{img_str}"

def on_connect(client, userdata, flags, rc):
    print(f"✅ Conectado al broker (Código: {rc})")
    client.subscribe(TOPIC)

cliente = mqtt.Client(MI_ID)
cliente.on_connect = on_connect
cliente.connect(BROKER, 1883)
cliente.loop_start()

foto_perfil_default = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAMAAABg3Am1AAAAM1BMVEUAAAD///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACT5v7FAAAAEHRSTlMAECBAQEBAMDAwMDAwMDAw7fS6pAAAAGBJREFUeNrt0bEOwCAIRVHu//9pG6vXqV2SSTvXFw5CggAAAAAAAAB4I5E5z+xZ6b5l5pxn9qx03zJzzjN7VrpvmTnnmT0r3bfMnPPMnpXuW2bOeWbP6llp5yUAAAAAAAAA+MAnD8wAn7b33pMAAAAASUVORK5CYII="

try:
    while True:
        msg = input("Mensaje o ruta de imagen: ")
        tipo = "texto"
        contenido = msg
        
        if msg.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            tipo = "imagen"
            contenido = procesar_imagen(msg)
            
        payload = {
            "tecnicoId": MI_ID,
            "nombre": "Aldo",
            "fotoPerfil": foto_perfil_default,
            "tipo": tipo,
            "mensaje": contenido
        }
        cliente.publish(TOPIC, json.dumps(payload))
except KeyboardInterrupt:
    cliente.disconnect()