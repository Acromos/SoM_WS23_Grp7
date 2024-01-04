from paho.mqtt import client as mqtt_client
from random import randint
import random
import numpy as np
import time

MQTT_PORT=1883
MQTT_ADDRESS="141.22.194.198"
MQTT_CLIENT_NAME="Diana_send"
MQTT_TOPIC="MEDS/Temperatur"

#Hier steht die Nachricht
while (True):
    
    text= np.random.uniform(low=0, high=90.0)
    text = str(text)

    #Send Text to MQTT
    client = mqtt_client.Client(MQTT_CLIENT_NAME)
    client.connect(MQTT_ADDRESS, MQTT_PORT)
    client.publish(MQTT_TOPIC, text)
    time.sleep(5)