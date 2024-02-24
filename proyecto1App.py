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

humidity_values = []
pressure_values = []

def get_data():
    global humidity_values, pressure_values
    response = requests.get(url=URL, params=PARAMS)
    data = json.loads(response.text)
    entries = data['feeds']

    timestamps = []
    temperatures = []

    for entry in entries:
        timestamps.append(entry['created_at'])
        temperatures.append(float(entry['field1']))
        humidity_values.append(float(entry['field2']))
        pressure_values.append(float(entry['field3']))

    return timestamps, temperatures

# Se crea la ventana para la aplicación de Tkinter
root = tk.Tk()
root.title("Gráfica de datos de sensores")

# Creamos figuras para las graficas
fig, axs = plt.subplots(3)

# Función que actualiza los datos y las graficas
def update(frame):
    timestamps, temperatures = get_data()

    axs[0].clear()
    axs[0].plot(timestamps, temperatures, label='Temperatura (Celsius)')
    axs[0].set_title('Temperatura')
    axs[0].legend()

    axs[1].clear()
    axs[1].plot(timestamps, humidity_values, label='Humedad (%)')
    axs[1].set_title('Humedad')
    axs[1].legend()

    axs[2].clear()
    axs[2].plot(timestamps, pressure_values, label='Presión (hPa)')
    axs[2].set_title('Presión')
    axs[2].legend()

    for ax in axs:
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Valor')
        ax.grid(True)

        canvas.draw()

#Creamos un lienzo con la libreria de matplotlib en la ventana que usamos de Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

#Actualizar los datos cada 5 segundos
ani = FuncAnimation(fig, update, interval=5000)

#Iniciar app
root.mainloop()
