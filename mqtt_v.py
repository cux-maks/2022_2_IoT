import requests
import re
from datetime import datetime as d

def getWeather():

	retV = []

	my_PTY = ["없음", "비", "비/눈", "눈", "소나기"]
	my_SKY = {1 : "맑음", 3 : "구름많음", 4 : "흐림"}

	time = d.now()
	now_h = str()
	if (time.hour >= 0 and time.hour < 2) or (time.hour < 24 and time.hour) >= 23: now_h = "2300"
	elif time.hour >= 2 and time.hour < 5: now_h = "0200"
	elif time.hour >= 5 and time.hour < 8: now_h = "0500"
	elif time.hour >= 8 and time.hour < 11: now_h = "0800"
	elif time.hour >= 11 and time.hour < 14: now_h = "1100"
	elif time.hour >= 14 and time.hour < 17: now_h = "1400"
	elif time.hour >= 17 and time.hour < 20: now_h = "1700"
	elif time.hour >= 20 and time.hour < 23: now_h = "2000"

	now_d = str(time.date())
	now_d = ''.join([x for x in list(now_d) if x != '-'])

	#print(now_h)
	#print(now_d)

	url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
	params = {'serviceKey' : 'JYVAfDor8zrqtfnqsihAVqSRYDQFh382sboRRIHQOFlvI5Beo/r6/0SWlywHrH3lSnGlJq64vn8LNpYVBGnDFg==', 'numOfRows' : '50', 'pageNo' : '1', 'dataType' : 'XML', 'base_date' : now_d, 'base_time' : now_h, 'nx' : '55', 'ny' : '127' }

	response = requests.get(url, params=params)
	response_str = response.content.decode('utf-8')
	#print(response_str)

	cnt = 0

	# 강수 확률 추출
	#print("강수 확률")
	for x in list(response_str.split('<items>')):
		if cnt == 1: 
			buf = []
			for y in x.split("</item>"):

				if len(re.findall("POP", y)) != 0:
					
					findall_result = re.findall(r'<fcstValue>[0-9]{2}</fcstValue>', y) + re.findall(r'<fcstValue>[0-9]{3}</fcstValue>', y) + re.findall(r'<fcstValue>[0-9]{1}</fcstValue>', y)
					findall_time = re.sub(r'[^0-9]', '', (re.findall(r'<fcstTime>[0-9]{4}</fcstTime>', y))[0])
					result_num = re.sub(r'[^0-9]', '', findall_result[0])
					# print("time: ", findall_time)
					#print(findall_time, "강수확률(POP):", result_num, "%")
					buf.append(str(findall_time) + " 강수확률(POP): " + str(result_num) + "%")
			retV.append(buf)
		cnt += 1

	cnt = 0
	# 강수 형태 추출
	#print("강수 형태")
	for x in list(response_str.split('<items>')):
		if cnt == 1: 
			buf = []
			for y in x.split("</item>"):

				if len(re.findall("PTY", y)) != 0:
					
					findall_result = re.findall(r'<fcstValue>[0-9]{1}</fcstValue>', y)
					findall_time = re.sub(r'[^0-9]', '', (re.findall(r'<fcstTime>[0-9]{4}</fcstTime>', y))[0])
					result_num = re.sub(r'[^0-9]', '', findall_result[0])
					# print("time: ", findall_time)
					#print(findall_time, "강수형태(PTY):", my_PTY[int(result_num)])
					buf.append(str(findall_time) + " 강수형태(PTY): " + my_PTY[int(result_num)])
			retV.append(buf)
		cnt += 1

	cnt = 0
	# 하늘 상태 추출
	#print("하늘 상태")
	for x in list(response_str.split('<items>')):
		if cnt == 1: 
			buf = []
			for y in x.split("</item>"):

				if len(re.findall("SKY", y)) != 0:
					
					findall_result = re.findall(r'<fcstValue>[0-9]{1}</fcstValue>', y)
					findall_time = re.sub(r'[^0-9]', '', (re.findall(r'<fcstTime>[0-9]{4}</fcstTime>', y))[0])
					result_num = re.sub(r'[^0-9]', '', findall_result[0])
					# print("time: ", findall_time)
					#print(findall_time, "하늘상태(SKY):", my_SKY[int(result_num)])
					buf.append(str(findall_time) + " 하늘상태(SKY): " + my_SKY[int(result_num)])
			retV.append(buf)
		cnt += 1
	
	return retV


a = getWeather()
for i in a:
	print(i)
