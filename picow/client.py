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


timer_started = False
timer_count = 1
timer_count_carga = 0
bpm = 0

MOTOR_PIN_16 = machine.Pin(16, machine.Pin.OUT) #IN1
MOTOR_PIN_17 = machine.Pin(17, machine.Pin.OUT) #IN2
MOTOR_PIN_18 = machine.Pin(18, machine.Pin.OUT) #IN3
MOTOR_PIN_19 = machine.Pin(19, machine.Pin.OUT) #IN4

timer = Timer(-1)




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


def inyeccion(t):
    global timer_count, timer_started, gpio26, timer_count_carga
    
    timer_count += 1
    
    
    if timer_count >= 300 and not timer_count_carga: #3 seg de inyeccion
        detener_motor()
        
        if timer_count == 3300: #30 seg para la proxima lectura
            timer_count = 1
            timer_started = False
            t.deinit()
    
    
    elif timer_count < 300 and not timer_count_carga: #inyeccion
        girar_antihorario()
        

    if timer_count_carga: #carga
        girar_horario()

    if timer_count == timer_count_carga + 600: #6 seg de carga
        timer_count_carga = 0
        timer_started = False
        t.deinit()
        detener_motor()

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
                if utime.ticks_diff(utime.ticks_ms(), start_time) > 5000:
                    print('No se pudo conectar en 5 segundos.')
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

s.settimeout(1)



while True:
    print("Esperando recibir datos...")
    
    
    try:
        # Intentar recibir los datos
        msg = s.recv(1024)
        bpm = msg.decode("utf-8")
        print("bpm recibido:", bpm)

        if gpio26.value() and timer_started != True:
            timer_count_carga = timer_count
            timer.init(period=10, mode=Timer.PERIODIC, callback=inyeccion)
            timer_started = True
        
        if bpm == "1" and timer_started != True:
            timer.init(period=10, mode=Timer.PERIODIC, callback=inyeccion)
            timer_started = True
            
        
    except OSError as e:
        print("Nada che =(")
        
