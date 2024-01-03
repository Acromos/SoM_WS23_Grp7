# Import von Modulen (Flask für eine Webanwendung mit Live-Plot von Daten)

from flask import Flask, render_template, Response
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import tkinter as tk
from matplotlib.figure import Figure
import random
from datetime import datetime
import threading
import csv
from io import StringIO
import paho.mqtt.client as mqtt
import time

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



# Objekt initialisieren
app = Flask(__name__)

# Beispiel-Daten ## Hier müssten die Daten aus dem read aufgerufen werden
x_data = [1, 2, 3, 4, 5]
y_data = [random.uniform(20, 30) for _ in range(len(x_data))]

# Matplotlib Figur wird erstellt und die Temperaturdaten geplottet
fig, ax = plt.subplots()
ax.plot(x_data, y_data)
ax.set_title('Temperaturanzeige')
canvas = FigureCanvas(fig)

# Plot wird als Bild gespeichert
temp_filename = 'temp_plot.png'
fig.savefig(temp_filename, bbox_inches='tight')
plt.close(fig)

def background_server_function(name):
    app.run(host='0.0.0.0', port=8080, debug=True)

# Mit dieser Funktion können die Daten stets aktualisiert werden/ Liveanpassung mit read verknüpfen
def update_plot():
    global x_data, y_data
    x_data.append(x_data[-1] + 1)
    y_data.append(random.uniform(20, 30))

    ax.plot(x_data[-2:], y_data[-2:])
    ax.set_title('Temperaturanzeige')

    # Speichere das aktualisierte Plot-Bild
    fig.savefig(temp_filename, bbox_inches='tight')
    plt.close(fig)

@app.route('/')
def index():
    return render_template('index.html', plot_image=temp_filename)

@app.route('/plot.png')
def plot():
    with open(temp_filename, 'rb') as f:
        image_binary = f.read()
    return Response(image_binary, mimetype='image/png')

# Route, wenn plot nur bei /update_plot aktualisiert werden soll ## de komplette Funktion muss noch überarbeitet werden
@app.route('/update_plot')
def update_and_plot():
    update_plot()
    return 'Plot aktualisiert!'

# Für die Mittelwert Berechnung
@app.route('/calculate_mean')
def calculate_mean():
    mean_value = sum(y_data) / len(y_data)
    ax.axhline(mean_value, color='red', linestyle='dashed', linewidth=2)
    canvas.draw()
    return f'Mittelwert: {mean_value:.2f}'

# Skala formattieren ##funktioniert noch nicht!!
@app.route('/format_scale')
def format_scale():
    # Umrechnung von Celsius zu Kelvin: K = C + 273.15
    ax.set_ylabel('Temperatur (Kelvin)')
    y_data_kelvin = [temp + 273.15 for temp in y_data]
    ax.clear()
    ax.plot(x_data, y_data_kelvin)
    ax.set_title('Temperaturanzeige (Kelvin)')
    canvas.draw()
    return 'Skala formatiert zu Kelvin'

@app.route('/download')
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


# Start the MQTT subscription in a separate thread
threading.Thread(target=temperature_update, daemon=True).start()

# Start the background server
threading.Thread(target=background_server_function, args=(1,), daemon=True).start()

# um Starten der Flask Webseite
if __name__ == '__main__':
    app.run(debug=True)