import threading
import time
from time import sleep
import socket
import select
import json
import dearpygui.dearpygui as dpg

bpm = 0
updated_bpm_value = 0
bpm_value = 0
value_lock = threading.Lock()

# Función para iniciar la interfaz gráfica de DearPyGui
def iniciar_grafico():
    global bpm_value

    
    
    
    dpg.create_context()
    dpg.create_viewport(title='BioBand CO', width=600, height=300)

    with dpg.font_registry():
        font_large = dpg.add_font("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 500)
        font_large1 = dpg.add_font("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 70)

    with dpg.window(label="BioBand-Health", width=600, height=300):
        prueba_text = dpg.add_text(default_value=str(bpm_value), pos=(450, 250))
        prueba_text1 = dpg.add_text("PULSACIONES POR MINUTO (BPM):", pos=(220, 70))
        dpg.add_text("Gracias por usar nuestro sistema", pos=(100, 900))
        dpg.bind_item_font(prueba_text, font_large)
        dpg.bind_item_font(prueba_text1, font_large1)

    dpg.setup_dearpygui()
    dpg.show_viewport()

    # Ciclo principal de DearPyGui
    while dpg.is_dearpygui_running():
        dpg.set_value(prueba_text, f"{bpm_value:.2f}")  # Actualizar la interfaz gráfica
        dpg.render_dearpygui_frame()
        
        
    dpg.destroy_context()


# Iniciar los hilos de la interfaz gráfica y la actualización del bpm_value
threading.Thread(target=iniciar_grafico, daemon=True).start()
        


# Función para manejar la conexión con el ESP32
def esp32(conn):
    global bpm
    global bpm_value
    print("ESP32 conectada")

    while True:
        try:
            bpm_data = conn.recv(1024)
            bpm_data = bpm_data.decode("utf-8")
            bpm = bpm_data  # Actualiza la variable global bpm con el dato recibido
            bpm_value = float(bpm)  # Convierte bpm a un número flotante
            #print(f"Valor de BPM recibido: {bpm_value}")
            sleep(1)  # Espera 1 segundo antes de recibir el siguiente valor
        except:
            print("No hay mensajes del ESP32")
            sleep(1)

# Función para manejar la conexión con Raspberry Pi
def raspberry(conn):
    global bpm_value

    while True:
        try:
            if bpm_value:
                try:
                    
                    if bpm_value > 120:
                        conn.send("1".encode("utf-8"))
                        print("Enviado: 1 a la PicoW")
                        sleep(1)
                    else:
                        conn.send("0".encode("utf-8"))
                        print("Enviado: 0 a la PicoW")
                        sleep(1)
                except ValueError:
                    print(f"Error: Valor no numérico recibido: {bpm}")
        except OSError as e:
            print(f"Error de conexión al enviar datos: {e}")
            sleep(1)
        except Exception as e:
            print(f"Error inesperado: {e}")
            sleep(1)

# Configuración del servidor de socket
host = ""
port = 8000

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
print("Server started. Waiting for connection...")
s.listen(5)

# Aceptar conexiones y crear hilos para manejar cada dispositivo
while True:
    c, addr = s.accept()
    print(f"Tarea nueva corriendo para IP {addr}")

    msg = c.recv(1024)
    msg = msg.decode("utf-8")
    print(msg)
    
    if msg == "rppico":
        thread = threading.Thread(target=raspberry, args=(c,))
        thread.start()

    elif msg == "esp32":
        thread = threading.Thread(target=esp32, args=(c,))
        thread.start()


