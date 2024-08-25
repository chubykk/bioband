import threading
import time
import socket

host = ""
port = 5000

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #avoid reuse error msg
s.bind((host,port))
print ("Server started. Waiting for connection...")
s.listen(5)
c, addr = s.accept()
def bucle1():
    while True:
        
        time.sleep(1)  # Espera 1 segundo
        
        #print ("Connection from: ",addr)
       # c.send(bytes("conectado", "utf-8"))
    print("Bucle 1 ejecutándose")

def bucle2():
    while True:
        
        time.sleep(1)  # Espera 1 segundo
        data = c.recv(1024)
        if not data:
            break
        value = data.decode()
        print ("Recibido: ",value)

        if value == "1":
            c.send(bytes("inyectar", "utf-8"))
        else:
            c.send(bytes("nada", "utf-8"))

    print("Bucle 2 ejecutándose")



# Crear dos hilos para los bucles
hilo1 = threading.Thread(target=bucle1)
hilo2 = threading.Thread(target=bucle2)

# Iniciar los hilos
hilo1.start()
hilo2.start()

# Esperar a que los hilos terminen (esto no ocurrirá en este caso)
hilo1.join()
hilo2.join()