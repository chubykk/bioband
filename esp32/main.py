from MAX30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM, MAX30105_FIFO_READ_PTR
from time import sleep
from machine import SoftI2C, Pin, Timer 
from utime import ticks_diff, ticks_us
import usocket as socket
import network
import errno




##esto es para poner un gpio de la esp en 3.3V para alimentar el sensor MAX30102

#gpio2 = Pin(2, Pin.OUT) 
#gpio2.value(1)
#if gpio2 == 1:
#    print("3.3V en gpio2")

MAX_HISTORY = 32
history = []
beats_history = []
beat = False
beats = 0
    
i2c = SoftI2C(sda=Pin(21),scl=Pin(22),freq=400000)
sensor = MAX30102(i2c=i2c)  # An I2C instance is required

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    # Fill in your network name (ssid) and password here:
    ssid = 'LabLSE'
    password = 'embebidos32'
    sta_if.connect(ssid, password)
    while not sta_if.isconnected():
        pass
print('network config:', sta_if.ifconfig())

router_ip = "192.168.0.100"
#router_ip = "192.168.125.54"
#router_ip = "192.168.127.246"
#host = '192.168.0.100'
port = 8000

s = socket.socket()
s.connect((router_ip, port))
print("Connected to",router_ip)



# Scan I2C bus to ensure that the sensor is connected
if hex(sensor.i2c_address) not in i2c.scan():
    print("Sensor not found.")
    
elif not (sensor.check_part_id()):
    # Check that the targeted sensor is compatible
    print("I2C device ID not corresponding to MAX30102 or MAX30105.")
    
else:
    print("Sensor connected and recognized.")

# It's possible to set up the sensor at once with the setup_sensor() method.
# If no parameters are supplied, the default config is loaded:
# Led mode: 2 (RED + IR)
# ADC range: 16384
# Sample rate: 400 Hz
# Led power: maximum (50.0mA - Presence detection of ~12 inch)
# Averaged samples: 8
# pulse width: 411
print("Setting up sensor with default configuration.", '\n')
sensor.setup_sensor()

# It is also possible to tune the configuration parameters one by one.
# Set the sample rate to 400: 400 samples/s are collected by the sensor
sensor.set_sample_rate(400)
# Set the number of samples to be averaged per each reading
sensor.set_fifo_average(8)
# Set LED brightness to a medium value
sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)
sensor.set_led_mode(2)
sleep(1)

# The readTemperature() method allows to extract the die temperature in °C    
print("Reading temperature in °C.", '\n')
print(sensor.read_temperature())

t_start = ticks_us()  # Starting time of the acquisition   

def display_bpm(t):
    global beats        
    print('BPM: ', beats)
    
    try:
        if beats:
            s.send(str(beats).encode('utf-8'))
        
    except:
        pass  
timer = Timer(-1)
#timer = Timer(period=2000, mode=Timer.PERIODIC, callback=display_bpm) #modificar esta linea depediendo de si es ESP o RP2 (RP2)
timer.init(period=2000, mode=Timer.PERIODIC, callback=display_bpm) #(ESP)

while True:    
    # The check() method has to be continuously polled, to check if
    # there are new readings into the sensor's FIFO queue. When new
    # readings are available, this function will put them into the storage.
    while True:
        try:
            sensor.check()
            break
        except OSError as e:
            # Si ocurre un error (como Errno 19), imprimimos un mensaje y seguimos intentando
            if e.errno == 19:
                print("Esperando reconexión con el sensor...")
            # Esperamos un momento antes de intentar de nuevo
            sleep(.5)

    # Check if the storage contains available samples
    if sensor.available():
        # Access the storage FIFO and gather the readings (integers)
        red_reading = sensor.pop_red_from_storage()
        ir_reading = sensor.pop_ir_from_storage()
        
        value = red_reading
        history.append(value)
        # Get the tail, up to MAX_HISTORY length
        history = history[-MAX_HISTORY:]
        minima = 0
        maxima = 0
        threshold_on = 0
        threshold_off = 0

        minima, maxima = min(history), max(history)

        threshold_on = (minima + maxima * 3) // 4   # 3/4
        threshold_off = (minima + maxima) // 2      # 1/2
        
        if value > 1000:
            if not beat and value > threshold_on:
                beat = True                    
                t_us = ticks_diff(ticks_us(), t_start)
                t_s = t_us/1000000
                f = 1/t_s
                bpm = f * 60
                if bpm < 500:
                    t_start = ticks_us()
                    beats_history.append(bpm)                    
                    beats_history = beats_history[-MAX_HISTORY:] 
                    beats = round(sum(beats_history)/len(beats_history) ,2)                    
            if beat and value< threshold_off:
                beat = False
            
        else:
            print('Not finger')




