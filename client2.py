import usocket as socket
import network

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    # Fill in your network name (ssid) and password here:
    ssid = 'Cooperadora Alumnos'
    password = ''
    wlan.connect(ssid, password)
    while not sta_if.isconnected():
        pass
print('network config:', sta_if.ifconfig())

router_ip = "192.168.127.246"
#host = '192.168.0.100'
port = 8000

s = socket.socket()
s.connect((router_ip,port))
print("Connected to",router_ip)


while True:
    message = input("->")
    s.send(message.encode())
    msg = s.recv(1024)
    print(msg.decode("utf-8"))
   
    #convert to bytes then send
