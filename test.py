import RPi.GPIO as gpio
import paho.mqtt.client as mqtt

pir_sens_pin = 21

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(pir_sens_pin, gpio.IN)

ip_address = "192.168.110.202"

mqttc = mqtt.Client()

mqtt_sub = ["gps", "hum", "PIR"]

def on_connect(client, userdata, flags, rc):
	print("Connected with result code" + str(rc))
	for i in mqtt_sub:
		mqttc.subscribe(i)

def on_publish(client, userdata, mid):
	msg_id = mid
	print("message published")
	
def on_message(client, userdata, msg):
	print("Topic:", msg.topic, " Message:", str(msg.payload))

mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_message = on_message

mqttc.connect(ip_address, 1883, 60)

try:
    while True:
        pir_state = gpio.input(pir_sens_pin)
        if pir_state:
            mqttc.publish("PIR", "detected")
        else:
            mqttc.publish("PIR", "nothing")
except KeyboardInterrupt:
	print("Finished")
	mqttc.disconnect()

'''
import RPi.GPIO as GPIO

try:
    while True:
        pir_state = GPIO.input(pir_sens_pin)
        if pir_state:
            print('detected')
        else:
            print('nothing')
except KeyboardInterrupt:
    GPIO.cleanup()
'''