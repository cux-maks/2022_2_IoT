import RPi.GPIO as gpio
import time

pir_sens_pin = 21

gpio.setmode(gpio.BCM)
gpio.setup(pir_sens_pin, gpio.IN)

try:
    while True:
        pir_state = gpio.input(pir_sens_pin)
        if pir_state:
            print('detected')
        else:
            print('nothing')
except KeyboardInterrupt:
    gpio.cleanup()