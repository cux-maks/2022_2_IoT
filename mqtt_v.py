import requests
import re as r
from datetime import datetime as d
import RPi.GPIO as gpio
import dht11
import math
import paho.mqtt.client as mqtt
import spidev

# import time

r_led = 5
y_led = 6
g_led =13

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(r_led, gpio.OUT)
gpio.setup(y_led, gpio.OUT)
gpio.setup(g_led, gpio.OUT)

gpio.output(r_led, False)
gpio.output(y_led, False)
gpio.output(g_led, False)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 976000

fsr_channel = 0

instance = dht11.DHT11(pin = 19)

ip_address = "192.168.110.202"

mqttc = mqtt.Client()

mqtt_sub = ["", "", ""]

hum_val = 30

NX = 149            ## X축 격자점 수
NY = 253            ## Y축 격자점 수

Re = 6371.00877     ##  지도반경
grid = 5.0          ##  격자간격 (km)
slat1 = 30.0        ##  표준위도 1
slat2 = 60.0        ##  표준위도 2
olon = 126.0        ##  기준점 경도
olat = 38.0         ##  기준점 위도
xo = 210 / grid     ##  기준점 X좌표
yo = 675 / grid     ##  기준점 Y좌표
first = 0

if first == 0 :
    PI = math.asin(1.0) * 2.0
    DEGRAD = PI/ 180.0
    RADDEG = 180.0 / PI

    re = Re / grid
    slat1 = slat1 * DEGRAD
    slat2 = slat2 * DEGRAD
    olon = olon * DEGRAD
    olat = olat * DEGRAD

    sn = math.tan(PI * 0.25 + slat2 * 0.5) / math.tan(PI * 0.25 + slat1 * 0.5)
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(PI * 0.25 + slat1 * 0.5)
    sf = math.pow(sf, sn) * math.cos(slat1) / sn
    ro = math.tan(PI * 0.25 + olat * 0.5)
    ro = re * sf / math.pow(ro, sn)
    first = 1

def dht():
	result = instance.read()
	if result.is_valid():
		return round(result.humidity, 3)
	else: return None

def mapToGrid(lat, lon, code = 0 ):
    ra = math.tan(PI * 0.25 + lat * DEGRAD * 0.5)
    ra = re * sf / pow(ra, sn)
    theta = lon * DEGRAD - olon
    if theta > PI :
        theta -= 2.0 * PI
    if theta < -PI :
        theta += 2.0 * PI
    theta *= sn
    x = (ra * math.sin(theta)) + xo
    y = (ro - ra * math.cos(theta)) + yo
    x = int(x + 1.5)
    y = int(y + 1.5)
    return x, y

def getWeather():

	retV = []

	find_V = ["POP", "PTY", "SKY"]
	append_V = [" 강수확률(POP): ", " 강수형태(PTY): ", " 하늘상태(SKY): "]
	last_V = ["%", "", ""]

	my_PTY = {"0":"없음", "1":"비", "2":"비/눈", "3":"눈", "4":"소나기"}
	my_SKY = {"1" : "맑음", "3" : "구름많음", "4" : "흐림"}

	time = d.now()
	now_h = str()
	if (time.hour > 0 and time.hour <= 2) or (time.hour <= 24 and time.hour > 23): now_h = "2300"
	elif time.hour > 2 and time.hour <= 5: now_h = "0200"
	elif time.hour > 5 and time.hour <= 8: now_h = "0500"
	elif time.hour > 8 and time.hour <= 11: now_h = "0800"
	elif time.hour > 11 and time.hour <= 14: now_h = "1100"
	elif time.hour > 14 and time.hour <= 17: now_h = "1400"
	elif time.hour > 17 and time.hour <= 20: now_h = "1700"
	elif time.hour > 20 and time.hour <= 23: now_h = "2000"

	realtime = str(time.hour) + "00"
	retV.append(realtime)
	
	now_d = str(time.date())
	now_d = ''.join([x for x in list(now_d) if x != '-'])

	# print(now_h)
	#print(now_d)

	x_n = 36.766615
	y_n = 127.282466
	
	nx, ny = mapToGrid(x_n, y_n)
	
	url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
	params = {'serviceKey' : 'JYVAfDor8zrqtfnqsihAVqSRYDQFh382sboRRIHQOFlvI5Beo/r6/0SWlywHrH3lSnGlJq64vn8LNpYVBGnDFg==', 'numOfRows' : '50', 'pageNo' : '1', 'dataType' : 'XML', 'base_date' : now_d, 'base_time' : now_h, 'nx' : str(nx), 'ny' : str(ny) }

	response = requests.get(url, params=params)
	response_str = response.content.decode('utf-8')
	#print(response_str)

	cnt = 0

	# 강수 확률 추출
	#print("강수 확률")
	for x in list(response_str.split('<items>')):
		if cnt >= 1: 
			
			for yp in x.split("</item>"):
				# print(y)
				for i in range(3):
					buf = []
					if len(r.findall(find_V[i], yp)) != 0:
						findall_result = r.findall(r'<fcstValue>[0-9]{2}</fcstValue>', yp) + r.findall(r'<fcstValue>[0-9]{3}</fcstValue>', yp) + r.findall(r'<fcstValue>[0-9]{1}</fcstValue>', yp)
						findall_time = r.sub(r'[^0-9]', '', (r.findall(r'<fcstTime>[0-9]{4}</fcstTime>', yp))[0])
						result_num = r.sub(r'[^0-9]', '', findall_result[0])
						# print("time: ", findall_time)
						#print(findall_time, "강수확률(POP):", result_num, "%")
						#if str(findall_time) == realtime: buf.append(str(findall_time) + " 강수확률(POP): " + str(result_num) + "%")
						if find_V[i] == "PTY": val = my_PTY[result_num]
						elif find_V[i] == "SKY": val = my_SKY[result_num]
						else: val = str(result_num)
						buf.append(str(findall_time) + append_V[i] + val + last_V[i])
						retV.append(buf)
		cnt += 1
	
	return retV

def on_connect(client, userdata, flags, rc):
	print("Connected with result code" + str(rc))
	for i in mqtt_sub:
		mqttc.subscribe(i)

def on_publish(client, userdata, mid):
	msg_id = mid
	print("message published")
	
def on_message(client, userdata, msg):
	print("Topic:", msg.topic, " Message:", str(msg.payload))
	if msg.topic == "PIR" and str(msg.payload) == "detected":
		if readChannel(fsr_channel) >= 10:
			mqttc.publish(mqtt_sub[0], "GPS")
	else:
		if readChannel(fsr_channel) >= 10:
			if dht() >= hum_val:
				gpio.output(r_led, True)
			else:
				gpio.output(r_led, False)
				
def readChannel(channel):
	adc = spi.xfer2([1, (8 + channel) << 4, 0])
	return ((adc[1] & 3) << 8) + adc[2]

mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_message = on_message

mqttc.connect(ip_address, 1883, 60)

try:
	mqttc.loop_forever()
except KeyboardInterrupt:
	print("Finished")
	for i in mqtt_sub: mqttc.unsubscribe(i)
	mqttc.disconnect()

'''
while True:
    fsr_level = readChannel(fsr_channel)
    prin(fsr_level)
'''
	
'''
a = getWeather()
print("time:", a[0])
for i in range(1, len(a) - 1, 3):
	print(a[i], a[i+1], a[i+2])
'''
	
# print(a)
# now_time = a[0]
# for i in a[1:]:
# 	for x in i:
# 		time = list(x)
# 		time = ''.join(time[x] for x in range(4))
# 		if time == now_time: print(x)
