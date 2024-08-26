import threading
import time
import socket

def task(conn):


    while True:

        data = conn.recv(1024)
        value = data.decode()

        if not value:
            print("Cliente desconectado")
            return
        
        print("Recibido: ", value)

        try:
            if value == "1":
                c.send(bytes("inyectar", "utf-8"))
            else:
                c.send(bytes("nada", "utf-8"))    
        
        except:
            pass



host = ""
port = 8000

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #avoid reuse error msg
s.bind((host,port))
print ("Server started. Waiting for connection...")
s.listen(5)

while True:

    c, addr = s.accept()
    thread = threading.Thread(target=task, args=(c,))
    thread.start()
    print(f"Tarea nueva corriendo para IP {addr}")
