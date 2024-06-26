import requests
import xmltodict
import json
from dotenv import load_dotenv
import os

from base_data.cheongan import CHEONGAN
from base_data.jiji import JIJI
from utils import utils as u


class SolarToLunarAPI:
    def __init__(self):
        # .env 파일 로드
        load_dotenv()

        # 환경 변수에서 API 호출 정보 불러오기
        self.endpoint = os.getenv('ENDPOINT')
        self.api_key = os.getenv('API_KEY')


    def get_time_pillar_info(self, date:str, time:str):
        """ 
        천간은 DATE 첫글짜를 뽑는다 => 병, idx=3
        => (시간 idx) + 2*(첫글자 idx%5-1) 번째 천간이 시작천간이 된다
        지지는 time의 시간이 바로 지지가 된다

        Args:
            date (str): "병신" or "병신(丙申)"
            time (str):"사시"
        """
        def find_time_cheongan(date:str, time:str):
            # date의 0번째 글자로천간의 idx를 추출한다.
            first_idx = CHEONGAN[date[0]]['idx']
            print('first_idx:', first_idx)
            time_jiji_idx =JIJI[time[0]]['idx']
            time_cheongan_idx = (time_jiji_idx)+ 2*(first_idx%5-1)
            print('time_cheongan_idx:', time_cheongan_idx)
            time_cheongan =u.get_item_by_idx(CHEONGAN, time_cheongan_idx)
            return time_cheongan
        
        cheongan = find_time_cheongan(date,time)
        jiji = JIJI[time[0]]
        time_str = f"{cheongan['korean']}{jiji['korean']}({cheongan['chinese']}{jiji['chinese']})"
        return time_str
    
    def get_solar_to_lunar_info(self, year: int, month: int, day: int):
        """_summary_

        Args:
            year (int): '1991'
            month (int): '07'
            day (int): '25'

        Returns:
            Dict: {'lunDay': '14', 'lunIljin': '병신(丙申)', 'lunLeapmonth': '평', 'lunMonth': '06', 'lunNday': '29', 'lunSecha': '신미(辛未)', 'lunWolgeon': '을미(乙未)', 'lunYear': '1991', 'solDay': '25', 'solJd': '2448463', 'solLeapyear': '평', 'solMonth': '07', 'solWeek': '목', 'solYear': '1991'}
        """
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
        
    def get_all_four_pillar_info(self, year: int, month: int, day: int, time:str):
        lunar_info = self.get_solar_to_lunar_info(year, month, day)
        time_str = self.get_time_pillar_info(lunar_info['lunIljin'],time)
        lunar_info['lunHour'] =time_str
        return lunar_info

# 예제 사용법
api = SolarToLunarAPI()
year = '1991'
month = '07'
day = '09'
time = "자시"
lunar_info = api.get_all_four_pillar_info(year, month, day, time)
print(lunar_info)