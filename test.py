import RPi.GPIO as GPIO

pir_sens_pin = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_sens_pin, GPIO.IN)

try:
    while True:
        pir_state = GPIO.input(pir_sens_pin)
        if pir_state:
            print('detected')
        else:
            print('nothing')
except KeyboardInterrupt:
    GPIO.cleanup()