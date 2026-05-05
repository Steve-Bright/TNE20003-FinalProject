import time
import random
import ssl
import json
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os

load_dotenv()

BROKER = os.getenv("BROKER")
PORT = int(os.getenv("PORT"))
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
STUDENT_ID = os.getenv("STUDENT_ID")

TEMP_TOPIC = f"{STUDENT_ID}/device1/temperature"
COMMAND_TOPIC = f"{STUDENT_ID}/device1/command"
PUBLIC_TOPIC = "public/#"

def on_connect(client, userdata, flags, reason_code, properties=None):
    print("================================")
    print("Cnnected:", reason_code)

    client.subscribe(COMMAND_TOPIC)
    client.subscribe(PUBLIC_TOPIC)

    print("--------------------------------")
    print("Subscriptions: ")
    print(COMMAND_TOPIC)
    print(PUBLIC_TOPIC)
    print("--------------------------------")

def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()

    print("\nDevice 1 received message")
    print("Topic:", topic)
    print("Payload:", payload)

    if topic == COMMAND_TOPIC:
        print("Device 1 action:", payload)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(USERNAME, PASSWORD)

client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
client.tls_insecure_set(True)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)
client.loop_start()

while True:
    temperature = round(random.uniform(25, 40), 2)

    data = {
        "device": "device1_sensor",
        "temperature": temperature,
        "unit": "C"
    }

    client.publish(TEMP_TOPIC, json.dumps(data), qos=0)

    print("\nDevice 1 published:")
    print("Topic:", TEMP_TOPIC)
    print("Data:", data)

    time.sleep(5)