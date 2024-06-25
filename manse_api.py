import requests
import xmltodict
import json
from dotenv import load_dotenv
import os

class SolarToLunarAPI:
    def __init__(self):
        # .env 파일 로드
        load_dotenv()

        # 환경 변수에서 API 호출 정보 불러오기
        self.endpoint = os.getenv('ENDPOINT')
        self.api_key = os.getenv('API_KEY')

    def get_lunar_solar_info(self, year: int, month: int, day: int):
        # 요청 URL 생성
        url = f"{self.endpoint}/getLunCalInfo"
        params = {
            'ServiceKey': self.api_key,
            'solYear': year,
            'solMonth': month,
            'solDay': day,
            '_type': 'xml'
        }
        
        # API 호출
        response = requests.get(url, params=params)
        if response.status_code == 200:
            # XML 응답을 dict로 변환
            xml_data = response.content

            dict_data = xmltodict.parse(xml_data)
            lunar_info = dict_data.get('response', {}).get('body', {}).get('items', {}).get('item', {})
            return lunar_info
        else:
            print(f"Error: {response.status_code}")
            return None

# # 예제 사용법
# api = SolarToLunarAPI()
# year = '1991'
# month = '07'
# day = '25'
# lunar_info = api.get_lunar_solar_info(year, month, day)
# print(lunar_info)