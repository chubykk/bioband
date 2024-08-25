import usocket as socket

import network   # handles connecting to WiFi

# Connect to network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Fill in your network name (ssid) and password here:
ssid = 'AracaLaVaca'
password = 'DCCB2431'
wlan.connect(ssid, password)

host = '192.168.1.43'
port = 5000

s = socket.socket()
s.connect((host,port))
print("Connected to",host)



   


while True:
    message = input("->")
    s.send(message.encode())
    msg = s.recv(1024)
    print(msg.decode("utf-8"))
   
    #convert to bytes then send

   