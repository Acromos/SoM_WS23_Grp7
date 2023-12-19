from paho.mqtt import client as mqtt_client
import time

MQTT_PORT=1883
MQTT_ADDRESS="141.22.194.198"
MQTT_CLIENT_NAME="Test_PiSub"
MQTT_TOPIC="Gruppenname/Kanal"
TICK_RATE_HZ=2
TICK_RATE=1/TICK_RATE_HZ

#Liste für die Nachrichten
message_queue = []
#Funktion die beim eintreffen einer Nachricht diese in eine Liste packt
def on_message(client, userdata, msg):
    message=msg.payload.decode()
    message_queue.append(message)
#Verbinden mit MQTT
client = mqtt_client.Client(MQTT_CLIENT_NAME)
client.connect(MQTT_ADDRESS,MQTT_PORT)
#Subscribe zum Thema und Funktion "on_message" hinzufügen
client.subscribe(MQTT_TOPIC)
client.on_message = on_message
#Für immer laufen lassen
client.loop_start()
while (True):
    last_value=""
    value_queue = []
    #Kurz warten
    time.sleep(TICK_RATE)
    #Wenn es noch neue Nachrichten gibt...
    while len(message_queue)>0:
        #...dann kopiere diese von der Empfangsliste in die Anzeige-Liste
        last_value=message_queue.pop()
        value_queue.append(last_value)
        print(last_value) 