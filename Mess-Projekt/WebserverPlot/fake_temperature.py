import paho.mqtt.client as mqtt
import time
import random

broker_address = "141.22.194.198"
topic = "fake_temperature"

def on_connect(client, userdata, flags, rc):
    print("Verbunden mit dem Broker. Result Code: " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect

print("Connecting to the broker...")
client.connect(broker_address, 1883, 60)
print("Connected successfully!")


while True:
    fake_temperature = random.uniform(20.0, 30.0)
    client.publish(topic, fake_temperature)
    print("Fake Temperature gesendet. Topic: {}, Wert: {}".format(topic, fake_temperature))
    time.sleep(5)
