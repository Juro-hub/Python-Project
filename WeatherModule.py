import requests
import json
from datetime import *
import time
import urllib

# json
# http://pythonstudy.xyz/python/article/205-JSON-%EB%8D%B0%EC%9D%B4%ED%83%80

# 날씨 API KEY
APIKEY = "15aa3a91826c811c431ab34af6099637"

# 켈빈 온도를 섭씨 온도로 변환하는 함수
k2c = lambda k: k - 273.15

# 날씨 API 클래스
class WeatherApi:    
    def __init__(self, apikey):
        self.apikey = apikey
        self.api = "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current&hourly&appid={key}" # 예보를 위한 url
        
        # 날씨 딕셔너리
        self.weather_dict = {}

        # 위도, 경도 딕셔너리
        self.city_dict = { "서울":[37.5683, 126.9778], "수원":[37.2911, 127.0089], "부산":[35.1028,129.0403],
                         "인천":[37.45, 126.4161], "대전":[36.333, 127.4167], "대구":[35.8, 128.55], "전주":[35.8219, 127.1489] }        

        # 날씨 상태 딕셔너리
        self.desc_dict = { "light rain":"가벼운 비", "overcast clouds":"흐린 구름", "moderate rain":"적당한 비", 
                          "overcast clouds":"흐린 구름", "broken clouds":"깨진 구름", "clear sky":"맑은 하늘" }
        
    # 위도, 경도로 질의
    def Query(self, latitude, longitude):
        # API의 URL 구성하기
        url = self.api.format(lat=latitude, lon=longitude, key=self.apikey)
        # API에 요청을 보내 데이터 추출하기
        r = requests.get(url)
        # 결과를 JSON 형식으로 변환하기
        data = json.loads(r.text)    

        i = 0
        for d in data["daily"]:            
            # 기온
            temp = k2c(d["temp"]["day"])
            # 날씨 상태
            for w in d["weather"]:
                desc = w["description"]
                # desc가 날씨 상태 딕셔너리에 있으면 (key error방지)
                if desc in self.desc_dict:
                    desc = self.desc_dict[desc] # 한국어로 새로 얻는다

            # 날씨 정보를 딕셔너리에 key("0"~"7")로 추가
            self.weather_dict[str(i)] = [temp, desc]
            i += 1

        return  self.weather_dict              

    # 도시이름으로 질의 (7일 예보) 
    def QueryCityWeek(self, name):                
        list = self.city_dict[name]
        return self.Query(list[0], list[1])

    # 도시이름으로 질의 (1일) 
    def QueryCityDay(self, name, day):        
        list = self.city_dict[name]
        self.Query(list[0], list[1])
        
        return self.weather_dict[str(day)]

if __name__ == '__main__':    
    wa = WeatherApi(APIKEY)
    weather_dict = wa.QueryCityWeek("서울")    

    # 0 ~ 7일 모두 출력
    list_key = weather_dict.keys() # "0" ~ "7"
    for key in list_key:
        temp, desc = weather_dict[key]
        print("%.1f %s" % (temp, desc))

    # 지정일 출력
    temp, desc = wa.QueryCityDay("전주", 7)
    print("%.1f %s" % (temp, desc))