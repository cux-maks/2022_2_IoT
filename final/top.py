import paho.mqtt.client as mqtt
import RPi.GPIO as gpio

pir = 21

gpio.setmode(gpio.BCM)
gpio.setup(pir, gpio.IN)

mqtt_sub = ["gps", "hum", "btn"]
ip_address = "192.168.110.202"

mqttc = mqtt.Client()

def pir_state():
    if gpio.input(pir) == True:
        return "detected"
    else:
        return "nothing"

def on_connect(client, userdata, flags, rc):
	print("Connected with result code" + str(rc))
	for i in mqtt_sub:
		mqttc.subscribe(i)

def on_publish(client, userdata, mid):
	msg_id = mid
	print("message published")
	
def on_message(client, userdata, msg):
	if msg.topic in mqtt_sub:
        print("Topic:", msg.topic, " Message:", str(msg.payload))

mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_message = on_message

mqttc.connect(ip_address, 1883, 60)

try:
    while True:
        pir_result = pir_state()
        if pir_result == "detected": mqttc.publish("pir", pir_state())
        mqttc.loop()
except KeyboardInterrupt:
    mqttc.disconnect()
    print("finished")