# Import von Modulen (Flask für eine Webanwendung mit Live-Plot von Daten)

from flask import Flask, render_template, Response
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import tkinter as tk
from matplotlib.figure import Figure
import random
from datetime import datetime

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

# um Starten der Flask Webseite
if __name__ == '__main__':
    app.run(debug=True)
