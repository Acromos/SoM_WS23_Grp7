import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import paho.mqtt.client as mqtt
from datetime import datetime
import matplotlib.dates as mdates
import webbrowser
from tkinter import filedialog
import csv

class TemperatureMonitoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Temperaturerfassung")

        # MQTT Server Daten
        self.MQTT_PORT = 1883                  
        self.MQTT_ADDRESS = "141.22.194.198"  # IP Adresse: 141.22.194.198/ Außerhalb der Hochschule unterscheidet sie sich
        self.MQTT_CLIENT_NAME = "diana_send"
        self.MQTT_TOPIC = "MEDS/Temperatur_real"
        self.MQTT_TOPIC2 = "MEDS/Datum"
        self.TICK_RATE_HZ = 2                  
        self.TICK_RATE = 1 / self.TICK_RATE_HZ  # Wie oft wird nach neuen Nachrichten überprüft

        # Daten zum Speichern
        self.Speicher = []
        self.Zeitstempel = []
        self.Timestamp_Liste = []
        self.Temperatur_Liste = []

        # Verbindung zum MQTT-Server herstellen
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(self.MQTT_ADDRESS, 1883, 60)
        self.client.subscribe(self.MQTT_TOPIC)
        self.client.subscribe(self.MQTT_TOPIC2)
        self.client.loop_start()

        # Erstelle einen Figure- und Subplot-Objekt außerhalb der Funktion
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.subplot = self.figure.add_subplot(1, 1, 1)

        # Erstelle ein Canvas-Objekt außerhalb der Funktion
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Fenster anpassen

        # Button zum Öffnen der Webseite hinzufügen
        self.webpage_button = tk.Button(self.root, text="Webseite öffnen", command=self.open_webpage)
        self.webpage_button.pack()
        
        # Button zum CSV-Erstellen
        self.create_csv_button = tk.Button(root, text="CSV erstellen", command=self.create_csv)
        self.create_csv_button.pack(pady=10)

        # GUI starten
        self.root.mainloop()

    def on_message(self, client, userdata, msg):
        # Konvertieren der Daten in eine Liste
        
        if msg.topic == self.MQTT_TOPIC:
            self.Temperatur_Liste.append(float(msg.payload))
        elif msg.topic == self.MQTT_TOPIC2:
            self.Timestamp_Liste.append((msg.payload.decode()))
    
        if len(self.Temperatur_Liste)>30 and len(self.Timestamp_Liste)>30:
            self.Temperatur_Liste.pop(0)
            self.Timestamp_Liste.pop(0)
        print(self.Temperatur_Liste)
        print(self.Timestamp_Liste)
        # data = [float(x) for x in msg.payload.decode().split(',')]

        # # Daten global speichern
        # if len(self.Speicher) > 30:
        #     del self.Speicher[0]
        #     del self.Zeitstempel[0]

        # self.Speicher.append(data)

        # # Zeitstempel hinzufügen
        # self.Zeitstempel.append(datetime.now())

        # Plot aktualisieren
        if len(self.Temperatur_Liste) == len(self.Timestamp_Liste):
            self.update_plot()

    def update_plot(self):
        # Alten plot löschen
        self.subplot.clear()

        # Neuer Plot
        self.subplot.plot(self.Timestamp_Liste, self.Temperatur_Liste, label='Datenreihe')

        # Datumsformat für x-Achse
        #self.subplot.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
        self.subplot.tick_params(axis='x', rotation=45)
        self.subplot.set_title('Temperaturerfassung')
        self.subplot.set_xlabel('Zeit')
        self.subplot.set_ylabel('Temperatur')
        self.subplot.legend()

        # Zeichnen
        self.canvas.draw()

    def create_csv(self):

        # Dialog für Dateispeicherort anzeigen
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

        # CSV-Datei erstellen
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Schreibe Kopfzeile
            writer.writerow(["Datum", "Uhrzeit"] + [f"Datenreihe_{i+1}" for i in range(len(self.Speicher[0]))])
            
            # Schreibe die Daten in Zeilen
            for timestamp, data_row in zip(self.Zeitstempel, self.Speicher):
                # Formatieren von Datum und Uhrzeit
                date_str = timestamp.strftime("%Y-%m-%d")
                time_str = timestamp.strftime("%H:%M:%S")

                # Schreibe Zeile in CSV
                writer.writerow([date_str, time_str] + data_row)


        # Erfolgsmeldung
        tk.messagebox.showinfo("Erfolg", f"CSV-Datei wurde erfolgreich erstellt: {file_path}")
        
    # Funktion zum Öffnen der Webseite im Standard-Webbrowser
    def open_webpage(self):
        webbrowser.open("http://141.22.36.248/")  # URL anpassen, wenn Port sich ändert

if __name__ == "__main__":
    root = tk.Tk()
    app = TemperatureMonitoringApp(root)