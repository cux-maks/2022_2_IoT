import paho.mqtt.client as mqtt

mqtt_sub = ["gps", "hum", "pir", "btn"]
ip_address = "102.168.110.202"

mqttc = mqtt.Client()

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
        mqttc.loop()
except KeyboardInterrupt:
    mqttc.disconnect()
    print("finished")