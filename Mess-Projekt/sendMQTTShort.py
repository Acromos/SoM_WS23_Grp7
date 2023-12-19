from paho.mqtt import client as mqtt_client
from random import randint

MQTT_PORT=1883
MQTT_ADDRESS="141.22.194.198"
MQTT_CLIENT_NAME="Diana_send"
MQTT_TOPIC="MEDS/Kanal"

#Hier steht die Nachricht
text="Hello World and Random Value: " + str(randint(1, 100))

#Send Text to MQTT
client = mqtt_client.Client(MQTT_CLIENT_NAME)
client.connect(MQTT_ADDRESS, MQTT_PORT)
client.publish(MQTT_TOPIC, text)