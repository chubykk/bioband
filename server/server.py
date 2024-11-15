import dearpygui.dearpygui as dpg
import threading
import time
import socket



value = 0

value_lock = threading.Lock()


def task(conn):

    global value
    while True:

        data = conn.recv(1024)
        value = float(data.decode('utf-8'))

        if not value:
            print("Cliente desconectado")
            return
        
        print("Recibido: ", value)
  
        try:
            if value > 60:
                c.send("1")  #mandar el aviso de que BPM > 180, como un "1"
            else:
                c.send("0")

        except:
            pass




def iniciar_grafico():
    dpg.create_context()
    dpg.create_viewport(title='BioBand CO', width=600, height=300)
    with dpg.font_registry():
        font_large = dpg.add_font("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 500)
        font_large1 = dpg.add_font("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 70)
    with dpg.window(label="BioBand-Health", width=600, height=300):
        dpg.add_text("Gracias por usar nuestro sistema", pos=(100, 900))
        prueba_text = dpg.add_text(default_value=value, pos=(450, 250))
        prueba_text1 = dpg.add_text("PULSACIONES POR MINUTO (BPM):", pos=(220, 70))
        dpg.bind_item_font(prueba_text, font_large)
        dpg.bind_item_font(prueba_text1, font_large1)

    dpg.setup_dearpygui()
    dpg.show_viewport()

    while dpg.is_dearpygui_running():
        with value_lock:
            dpg.set_value(prueba_text, f"{value:.2f}")
        dpg.render_dearpygui_frame()

    dpg.destroy_context()

# Función para actualizar el gráfico en DearPyGui
def update_graph():

    if value:
        dpg.set_value([list(range(len(value))), value])








host = ""
port = 8000

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #avoid reuse error msg
s.bind((host,port))
print ("Server started. Waiting for connection...")
s.listen(5)

threading.Thread(target=iniciar_grafico, daemon=True).start()




while True:
    c, addr = s.accept()
    thread = threading.Thread(target=task, args=(c,))
    thread.start()
    print(f"Tarea nueva corriendo para IP {addr}")