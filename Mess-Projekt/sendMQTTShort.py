from paho.mqtt import client as mqtt_client
from random import randint

MQTT_PORT=1883
MQTT_ADDRESS="141.22.194.198"
MQTT_CLIENT_NAME="Test_PiPub"
MQTT_TOPIC="Gruppenname/Kanal"

#Hier steht die Nachricht
text="Random Value: " + str(randint(1, 100))

#Send Text to MQTT
client = mqtt_client.Client(MQTT_CLIENT_NAME)
client.connect(MQTT_ADDRESS, MQTT_PORT)
client.publish(MQTT_TOPIC, text)