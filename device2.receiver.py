import ssl
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os

load_dotenv()


BROKER = os.getenv("BROKER")
PORT = int(os.getenv("PORT"))
USERNAME = os.getenv("STUDENT_ID")
PASSWORD = os.getenv("STUDENT_ID")
STUDENT_ID = os.getenv("STUDENT_ID")

TEMP_TOPIC = f"{STUDENT_ID}/device1/temperature"
PUBLIC_TOPIC = "public/#"

def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Device 2 connected:", reason_code)

    client.subscribe(TEMP_TOPIC)
    client.subscribe(PUBLIC_TOPIC)

    print("Device 2 subscribed to:")
    print(TEMP_TOPIC)
    print(PUBLIC_TOPIC)

def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()

    print("\nDevice 2 received message")
    print("Topic:", topic)
    print("Payload:", payload)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(USERNAME, PASSWORD)

client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
client.tls_insecure_set(True)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)
client.loop_forever()