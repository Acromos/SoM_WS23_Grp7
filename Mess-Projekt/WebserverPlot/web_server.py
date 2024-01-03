from bottle import response, route, run
import threading
import time
import csv
from io import StringIO
import paho.mqtt.client as mqtt

temperature_data = []  # Here we store the temperature data

def on_connect(client, userdata, flags, rc):
    print("Connected to the MQTT broker with result code " + str(rc))
    client.subscribe("fake_temperature")

def on_message(client, userdata, msg):
    temperature = float(msg.payload.decode())
    add_temperature_data(temperature)

def temperature_update():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("141.22.194.198", 1883, 60)

    client.loop_forever()

def background_server_function(name):
    run(host='0.0.0.0', port=8080, debug=True)

@route('/hello')
def hello():
    return f"Live Temperature: {temperature_data[-1] if temperature_data else 'No data available'}"

@route('/download')
def download():
    # Create CSV data
    csv_data = StringIO()
    csv_writer = csv.writer(csv_data)
    csv_writer.writerow(['Timestamp', 'Temperature'])

    # Ensure temperature_data is not empty before writing rows
    if temperature_data:
        for entry in temperature_data:
            csv_writer.writerow([entry['timestamp'], entry['temperature']])

    # Save CSV data to a file (you might want to customize the filename)
    filename = 'temperature_data.csv'
    with open(filename, 'w') as file:
        file.write(csv_data.getvalue())

    # Offer CSV data as a download
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    return csv_data.getvalue()

# Function to add temperature data
def add_temperature_data(temperature):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    temperature_data.append({'timestamp': timestamp, 'temperature': temperature})

# Start the background server
threading.Thread(target=background_server_function, args=(1,), daemon=True).start()

# Start the MQTT subscription in a separate thread
threading.Thread(target=temperature_update, daemon=True).start()

# Run the Bottle application
run()
