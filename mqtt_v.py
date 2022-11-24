import requests
import re

url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
params ={'serviceKey' : 'JYVAfDor8zrqtfnqsihAVqSRYDQFh382sboRRIHQOFlvI5Beo/r6/0SWlywHrH3lSnGlJq64vn8LNpYVBGnDFg==', 'numOfRows' : '50', 'pageNo' : '1', 'dataType' : 'XML', 'base_date' : '20221121', 'base_time' : '1700', 'nx' : '55', 'ny' : '127' }

response = requests.get(url, params=params)
response_str = response.content.decode('utf-8')
#print(response_str)

cnt = 0

# 강수 확률 추출
print("강수 확률")
for x in list(response_str.split('<items>')):
    if cnt == 1: 
        for y in x.split("</item>"):

            if len(re.findall("POP", y)) != 0:
                
                findall_result = re.findall(r'<fcstValue>[0-9]{2}</fcstValue>', y) + re.findall(r'<fcstValue>[0-9]{3}</fcstValue>', y)
                findall_time = re.sub(r'[^0-9]', '', (re.findall(r'<fcstTime>[0-9]{4}</fcstTime>', y))[0])
                result_num = re.sub(r'[^0-9]', '', findall_result[0])
                print("time: ", findall_time)
                print("result: ", result_num)

            
    cnt += 1

cnt = 0
# 강수 형태 추출
print("강수 형태")
for x in list(response_str.split('<items>')):
    if cnt == 1: 
        for y in x.split("</item>"):

            if len(re.findall("PTY", y)) != 0:
                
                findall_result = re.findall(r'<fcstValue>[0-9]{1}</fcstValue>', y)
                findall_time = re.sub(r'[^0-9]', '', (re.findall(r'<fcstTime>[0-9]{4}</fcstTime>', y))[0])
                result_num = re.sub(r'[^0-9]', '', findall_result[0])
                print("time: ", findall_time)
                print("result: ", result_num)

            
    cnt += 1

cnt = 0
# 하늘 상태 추출
print("하늘 상태")
for x in list(response_str.split('<items>')):
    if cnt == 1: 
        for y in x.split("</item>"):

            if len(re.findall("SKY", y)) != 0:
                
                findall_result = re.findall(r'<fcstValue>[0-9]{1}</fcstValue>', y)
                findall_time = re.sub(r'[^0-9]', '', (re.findall(r'<fcstTime>[0-9]{4}</fcstTime>', y))[0])
                result_num = re.sub(r'[^0-9]', '', findall_result[0])
                print("time: ", findall_time)
                print("result: ", result_num)

            
    cnt += 1
