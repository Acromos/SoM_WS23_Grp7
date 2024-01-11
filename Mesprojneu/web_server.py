from flask import Flask, render_template, Response, make_response, send_file
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt
import threading
import time
import csv
from io import StringIO, BytesIO

MQTT_PORT = 1883
MQTT_ADDRESS = "141.22.194.198"
MQTT_CLIENT_NAME = "diana_send"
MQTT_TOPIC = "MEDS/Temperatur_real"
TICK_RATE_HZ = 2
TICK_RATE = 1 / TICK_RATE_HZ

# Initialize Flask app
app = Flask(__name__)

# Initialize temperature data list
temperature_data = []

# Initialize Matplotlib Figure and Axis
fig, ax = plt.subplots()
ax.set_title('Temperaturverlauf')
ax.set_xlabel('Zeit')
ax.set_ylabel('Temperatur (°C)')
canvas = FigureCanvas(fig)

# MQTT connection callback
def on_connect(client, userdata, flags, rc):
    print("Connected to the MQTT broker with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

# MQTT message callback
def on_message(client, userdata, msg):
    temperature = float(msg.payload.decode())
    add_temperature_data(temperature)

# Function to add temperature data
def add_temperature_data(temperature):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    temperature_data.append({'Timestamp': timestamp, 'Temperature': temperature})

# MQTT temperature update thread
def temperature_update():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_ADDRESS, MQTT_PORT, 60)
    client.loop_forever()

# Function to update plot
def update_plot():
    ax.clear()
    x_data = [entry['Timestamp'] for entry in temperature_data[-30:]]
    y_data = [entry['Temperature'] for entry in temperature_data[-30:]]
    ax.plot(x_data, y_data, marker='o', linestyle='-', color='b', label='Temperaturverlauf')
    ax.set_title('Temperaturverlauf')
    ax.set_xlabel('Zeit')
    ax.set_ylabel('Temperatur (°C)')
    ax.legend()

# Flask route for index page
@app.route('/')
def index():
    return render_template('index.html')

# Flask route for updating plot
@app.route('/update_plot')
def update_and_plot():
    update_plot()
    canvas.draw()
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

# Flask route for downloading CSV data
@app.route('/download')
def download():
    csv_data = StringIO()
    csv_writer = csv.writer(csv_data)
    csv_writer.writerow(['Timestamp', 'Temperature'])

    if temperature_data:
        for entry in temperature_data:
            csv_writer.writerow([entry['Timestamp'], entry['Temperature']])

    filename = 'temperature_data.csv'
    with open(filename, 'w') as file:
        file.write(csv_data.getvalue())

    response = make_response(csv_data.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    return response

if __name__ == '__main__':
    # Start MQTT thread in the main thread
    threading.Thread(target=temperature_update, daemon=True).start()

    # Run Flask app in the main thread without debug mode
    app.run(host='0.0.0.0', port=5000)
