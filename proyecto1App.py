import requests
from typing import Final
from dotenv import load_dotenv
import os
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Aquí se va a definir la clave de lectura que usa el canal de ThingSpeak
load_dotenv()

READ_API_KEY: Final[str] = os.getenv('READ_API_KEY')
SECRET_CHANNEL_ID: Final[str] = os.getenv('SECRET_CHANNEL_ID')

# Aquí va la url del API REST
URL = f'https://api.thingspeak.com/channels/{SECRET_CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=2'

# Definir los parametros de la peticion.
PARAMS = {'api_key': READ_API_KEY, 'results': 10}  # Últimos 10 registros.


def get_data():
    global humidity_values, pressure_values
    response = requests.get(url=URL, params=PARAMS)
    data = json.loads(response.text)
    entries = data['feeds']

    timestamps = []
    temperatures_DHT = []
    avg_temperatures_DHT = []
    humidity_values = []
    avg_humidity_values=[] 
    temperatures_BMP = []
    avg_temperatures_BMP = []
    pressure_values = []
    avg_pressure_values = []

    for entry in entries:
        timestamps.append(entry['created_at'])
        temperatures_DHT.append(float(entry.get('field1', 0)))
        avg_temperatures_DHT.append(float(entry.get('field2', 0)))
        humidity_values.append(float(entry.get('field3', 0)))
        avg_humidity_values.append(float(entry.get('field4', 0)))
        temperatures_BMP_value = entry.get('field5', None)
        if temperatures_BMP_value is not None:
            temperatures_BMP.append(float(temperatures_BMP_value))
        else:
            temperatures_BMP.append(0)
        avg_temperatures_BMP_value = entry.get('field6', None)
        if avg_temperatures_BMP_value is not None:
            avg_temperatures_BMP.append(float(avg_temperatures_BMP_value))
        else:
            avg_temperatures_BMP.append(0)
        pressure_values_value = entry.get('field7', None)
        if pressure_values_value is not None:
            pressure_values.append(float(pressure_values_value))
        else:
            pressure_values.append(0)
        avg_pressure_values_value = entry.get('field8', None)
        if avg_pressure_values_value is not None:
            avg_pressure_values.append(float(avg_pressure_values_value))
        else:
            avg_pressure_values.append(0)

    return timestamps,temperatures_DHT,avg_temperatures_DHT,humidity_values,avg_humidity_values,temperatures_BMP,avg_temperatures_BMP, pressure_values,avg_pressure_values


# Se crea la ventana para la aplicación de Tkinter
root = tk.Tk()
root.title("Gráfica de datos de sensores")

# Creamos figuras para las graficas
fig, axs = plt.subplots(4, 2, figsize=(12, 16))

# Ajustar el espaciado entre los gráficos
plt.subplots_adjust(hspace=0.5)

# Función que actualiza los datos y las graficas
def update(frame):
    timestamps, temperatures_DHT, avg_temperatures_DHT, humidity_values, avg_humidity_values, temperatures_BMP, avg_temperatures_BMP, pressure_values, avg_pressure_values = get_data()
    
    axs[0, 0].clear()
    axs[0, 0].plot(timestamps, temperatures_DHT, label='Temperatura DHT (Celsius)')
    axs[0, 0].set_title('Temperatura DHT')
    axs[0, 0].legend()

    axs[1, 0].clear()
    axs[1, 0].plot(timestamps, avg_temperatures_DHT, label='Temperatura promedio DHT (Celsius)')
    axs[1, 0].set_title('Temperatura DHT promedio')
    axs[1, 0].legend()

    axs[2, 0].clear()
    axs[2, 0].plot(timestamps, humidity_values, label='Humedad (%)')
    axs[2, 0].set_title('Humedad')
    axs[2, 0].legend()

    axs[3, 0].clear()
    axs[3, 0].plot(timestamps, avg_humidity_values, label='Humedad promedio')
    axs[3, 0].set_title('Humedad Promedio')
    axs[3, 0].legend()

    axs[0, 1].clear()
    axs[0, 1].plot(timestamps, temperatures_BMP, label='Temperatura BMP (Celsius)')
    axs[0, 1].set_title('Temperatura BMP')
    axs[0, 1].legend()

    axs[1, 1].clear()
    axs[1, 1].plot(timestamps, avg_temperatures_BMP, label='Temperatura promedio BMP (Celsius)')
    axs[1, 1].set_title('Temperatura Promedio BMP')
    axs[1, 1].legend()

    axs[2, 1].clear()
    axs[2, 1].plot(timestamps, pressure_values, label='Presión (hPa)')
    axs[2, 1].set_title('Presión')
    axs[2, 1].legend()

    axs[3, 1].clear()
    axs[3, 1].plot(timestamps, avg_pressure_values, label='Presión promedio (hPa)')
    axs[3, 1].set_title('Presión promedio')
    axs[3, 1].legend()

    for ax in axs.flat:
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Valor')
        ax.grid(True)

    canvas.draw()

# Creamos un lienzo con la libreria de matplotlib en la ventana que usamos de Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Actualizar los datos cada 5 segundos
ani = FuncAnimation(fig, update, interval=5000)

# Iniciar app
root.mainloop()
