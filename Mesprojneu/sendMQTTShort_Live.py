import time
import board
import adafruit_dht
from paho.mqtt import client as mqtt_client
from datetime import datetime

# MQTT-Konfiguration
MQTT_PORT = 1883
MQTT_ADDRESS = "141.22.194.198"
MQTT_CLIENT_NAME = "diana_send"
MQTT_TOPIC_TEMPERATURE = "MEDS/Temperatur_real"
MQTT_TOPIC_HUMIDITY = "MEDS/Luftfeuchtigkeit"
MQTT_TOPIC_DATUM = "MEDS/Datum"


# Initialisieren Sie das DHT-Gerät, wobei der Datenpin mit Pin 16 (GPIO 23) des Raspberry Pi verbunden ist:
dhtDevice = adafruit_dht.DHT11(board.D23)

# Erstellen Sie eine Instanz des MQTT-Clients
client = mqtt_client.Client(MQTT_CLIENT_NAME)
client.connect(MQTT_ADDRESS, MQTT_PORT)

while True:
    try:
        # Lesen der Werte vom DHT-Sensor
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Senden von Temperaturdaten an MQTT
        client.publish(MQTT_TOPIC_TEMPERATURE, str(temperature_c))

        # Senden von Luftfeuchtigkeitsdaten an MQTT
        client.publish(MQTT_TOPIC_HUMIDITY, str(humidity))

        # Senden von Datum Daten an MQTT
        client.publish(MQTT_TOPIC_DATUM, str(date_time))

        print("Temp: {:.2f} C    Humidity: {}% ".format(temperature_c, humidity))

    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)
