import usocket as socket
import _thread 
import machine
import utime
from time import sleep
from machine import Pin
from machine import Timer
import network
import select
import errno


## para "cargar" la jeringa con un boton en el gpio 26, haciendo que el motor gire hacia el otro lado
    
gpio26 = Pin(26, Pin.IN)



c = 0
a = 0
h = 0
reset = 0
bpm = 0

MOTOR_PIN_16 = machine.Pin(16, machine.Pin.OUT) #IN1
MOTOR_PIN_17 = machine.Pin(17, machine.Pin.OUT) #IN2
MOTOR_PIN_18 = machine.Pin(18, machine.Pin.OUT) #IN3
MOTOR_PIN_19 = machine.Pin(19, machine.Pin.OUT) #IN4



def girar_horario(): # con esta se carga
    secuencia_horaria = [1, 2, 4, 8]

    for i in range(4):
        MOTOR_PIN_16.value(secuencia_horaria[i] & 0x01)
        MOTOR_PIN_17.value(secuencia_horaria[i] & 0x02)
        MOTOR_PIN_18.value(secuencia_horaria[i] & 0x04)
        MOTOR_PIN_19.value(secuencia_horaria[i] & 0x08)

        utime.sleep_ms(3)  # Puedes ajustar la velocidad aquí

def girar_antihorario(): # con esta se inyecta
    secuencia_antihoraria = [8, 4, 2, 1]

    for i in range(4):
        MOTOR_PIN_16.value(secuencia_antihoraria[i] & 0x01)
        MOTOR_PIN_17.value(secuencia_antihoraria[i] & 0x02)
        MOTOR_PIN_18.value(secuencia_antihoraria[i] & 0x04)
        MOTOR_PIN_19.value(secuencia_antihoraria[i] & 0x08)

        utime.sleep_ms(3)  # Puedes ajustar la velocidad aquí

def detener_motor():
    # Detiene el motor estableciendo todas las señales de control en 0
    MOTOR_PIN_16.value(0)
    MOTOR_PIN_17.value(0)
    MOTOR_PIN_18.value(0)
    MOTOR_PIN_19.value(0)

def contador(t):
    global c
    c = c+1

def contador2(t):
    global a
    a = a+1
    
def contador3(t):
    global h
    h = h+1

timer = Timer(-1)
timer2 = Timer(-1)
timer3 = Timer(-1)

sta_if = network.WLAN(network.STA_IF)
# Intentos de conexión hasta que se logre
connected = False

while True:  # Bucle principal que se ejecutará indefinidamente
    if not sta_if.isconnected():
        print('Intentando conectar a la red...')
        sta_if.active(True)  # Asegurarse de que la interfaz está activa
        ssid = 'LabLSE'  # Tu red Wi-Fi
        password = 'embebidos32'  # Contraseña de tu red Wi-Fi
        
        connected = False
        while not connected:
            sta_if.connect(ssid, password)  # Intentar conectar
            start_time = utime.ticks_ms()  # Registrar el tiempo de inicio
            while not sta_if.isconnected():
                # Esperar hasta que se conecte o hayan pasado 15 segundos
                if utime.ticks_diff(utime.ticks_ms(), start_time) > 15000:
                    print('No se pudo conectar en 15 segundos.')
                    sta_if.active(False)  # Desactivar la interfaz de red
                    print('Interfaz desactivada. Reintentando...')
                    
                    # Esperar un momento antes de volver a activar la interfaz
                    sleep(2)  # Espera de 2 segundos antes de reactivar

                    # Volver a activar la interfaz de red
                    sta_if.active(True)
                    break  # Salir del bucle y reintentar la conexión

            # Si se logró conectar, salimos del bucle
            if sta_if.isconnected():
                connected = True
                print('Conectado a la red Wi-Fi:', ssid)
                print('Configuración de red:', sta_if.ifconfig())

    else:
        print('Ya estás conectado a la red.')
        break  # Salir del bucle si ya está conectado

#router_ip = "192.168.1.42"
#router_ip = "192.168.127.134"
#router_ip = "192.168.125.54"
#router_ip = "127.0.0.1"
#host = '192.168.0.100'
router_ip = "192.168.0.100"
port = 8000

s = socket.socket()
s.connect((router_ip, port))
print("Connected to",router_ip)
myid = "rppico"
s.send(myid.encode("utf-8"))
#s.setblocking(0)
s.settimeout(5)


def comunicacion():
    global bpm
    global s
  
    while True:
        print("Esperando recibir datos...")
        
        # select() espera hasta que haya datos disponibles para leer.
        #ready = select.select([s], [], [], 1)# Timeout de 1 segundo

        #if ready[0]:  # Si hay datos disponibles para leer
        try:
            # Intentar recibir los datos
            msg = s.recv(1024)
            bpm = msg.decode("utf-8")
            print("bpm recibido:", bpm)

        except OSError as e:
            print(e)

            
def inyeccion():
    global c
    global a
    global h
    global reset
    global bpm
    global timer
    while True:
       
           
        cargar = gpio26.value()
       
       
        
        if c == 0 and cargar == 1: #carga
            
            timer.init(period=100, mode=Timer.PERIODIC, callback=contador)
            
        if 0 < c < 50:
          
            girar_horario()
            
              
        if c > 50:
            
            timer.deinit()
            c = 0
            detener_motor()
        
        
        
        
        


        if bpm == "1" and reset == 0: #inyeccion
            
            print("inyecta")
            timer2.init(period=100, mode=Timer.PERIODIC, callback=contador2) #timer 5 seg para la inyeccion
            timer3.init(period=100, mode=Timer.PERIODIC, callback=contador3)#timer 1 min para el reset
            reset = 1
            
            
            
        if h > 600: #reset
            timer3.deinit()
            h = 0
            reset = 0
               
               
        if 0 < a < 50: #inyeccion
            
            girar_antihorario()
           
            
        if a > 50:
            
            timer2.deinit()
            a = 0
            detener_motor()
                
       
        
    
    
_thread.start_new_thread(inyeccion, ())
comunicacion()

# Ejecutar la función de inyección en el hilo principal


while True:
    pass

