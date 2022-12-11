import paho.mqtt.client as mqtt
import RPi.GPIO as gpio
import Adafruit_DHT as dht
import time

trig_pin = 13
echo_pin = 19
dht_pin = 21
led_pin = 5

gpio.setmode(gpio.BCM)
gpio.setup(trig_pin, gpio.OUT)
gpio.setup(echo_pin, gpio.IN)
gpio.setup(led_pin, gpio.OUT)

sensor = dht.DHT22

def getDis():
        gpio.output(trig_pin, False)
        time.sleep(0.5)

        gpio.output(trig_pin, True)
        time.sleep(0.00001)
        gpio.output(trig_pin, False)

        while gpio.input(echo_pin) == 0:
                pulse_start = time.time()

        while gpio.input(echo_pin) == 1:
                pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 34000 / 2
        distance = round(distance, 2)

        return distance

def getHum():
        humid, temp = dht.read_retry(sensor, dht_pin)
        return humid


def goenJoGi():
        gpio.output(led_pin, False)
        humid = getHum()
        print("humidity:", humid)
        while humid >= 35:
                gpio.output(led_pin, True)
                while(humid>=35):
                        humid = getHum()
                        print("humidity:",humid)
                gpio.output(led_pin, False)

        return

ip_address = "192.168.110.202"

mqttc = mqtt.Client()

def on_connect(client, userdata, flags, rc):
        print("Connected with result code" + str(rc))

def on_publish(client, userdata, mid):
        msg_id = mid
        print("message published")

def on_message(client, userdata, msg):
        if msg.topic in mqtt_sub:
                print("Topic:", msg.topic, " Message:", str(msg.payload))

mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

mqttc.connect(ip_address, 1883, 60)

try:
        while True:
                distance = getDis()
                print(distance)
                if distance < 5:
                        goenJoGi()
                        mqttc.publish("distance", distance)
except KeyboardInterrupt:
        mqttc.disconnect()
        print("finished")