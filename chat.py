import paho.mqtt.client as mqtt
import base64
import json
import io
from PIL import Image

BROKER = "broker.hivemq.com"
TOPIC = "clase/redes/equipo2/whatsapp_final_v3"
MI_ID = "Python_User"

# --- FUNCIÓN PARA COMPRIMIR IMÁGENES ---
def procesar_imagen(ruta_imagen, es_perfil=False):
    # Abrir la imagen
    with Image.open(ruta_imagen) as img:
        # Si es perfil la hacemos miniatura (100x100), si es chat (400x400)
        size = (100, 100) if es_perfil else (400, 400)
        img.thumbnail(size)
        
        # Convertir a RGB (por si es PNG con transparencia)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        # Guardar en un buffer de memoria como JPEG comprimido
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=60) # Calidad 60 para que sea muy ligero
        
        # Convertir a Base64
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/jpeg;base64,{img_str}"

# --- CONFIGURACIÓN MQTT ---
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        if data["tecnicoId"] != MI_ID:
            print(f"\n[{data['nombre']}]: {data['mensaje'] if data['tipo'] == 'texto' else 'sent an image'}")
    except:
        pass

cliente = mqtt.Client(MI_ID)
cliente.on_message = on_message
cliente.connect(BROKER, 1883)
cliente.subscribe(TOPIC)
cliente.loop_start()

print("✅ Python Chat Activo con Compresor")

try:
    # Foto de perfil inicial
    foto_perfil = "https://cdn-icons-png.flaticon.com/512/149/149071.png"
    
    while True:
        opcion = input("\n1. Enviar Texto\n2. Enviar Imagen\n3. Cambiar Foto Perfil\n> ")
        
        if opcion == "1":
            msj = input("Mensaje: ")
            payload = {
                "tecnicoId": MI_ID,
                "nombre": "Aldo_Python",
                "fotoPerfil": foto_perfil,
                "tipo": "texto",
                "mensaje": msj
            }
            cliente.publish(TOPIC, json.dumps(payload))
            
        elif opcion == "2":
            ruta = input("Ruta de la imagen (ej: foto.jpg): ")
            try:
                img_b64 = procesar_imagen(ruta)
                payload = {
                    "tecnicoId": MI_ID,
                    "nombre": "Aldo_Python",
                    "fotoPerfil": foto_perfil,
                    "tipo": "imagen",
                    "mensaje": img_b64
                }
                cliente.publish(TOPIC, json.dumps(payload))
                print("¡Imagen enviada y comprimida!")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "3":
            ruta = input("Ruta de tu nueva foto de perfil: ")
            try:
                foto_perfil = procesar_imagen(ruta, es_perfil=True)
                print("Foto de perfil actualizada (comprimida).")
            except Exception as e:
                print(f"Error: {e}")

except KeyboardInterrupt:
    cliente.disconnect()