# 먼저 오픈다트 공시정보 중 공시 대상 기업 고유번호들을 받아서 정리하고
# (약 9만개)
# 위 고유번호들 중 상장회사가 아닌 것들을 제외하여 다시 정리하고
# (약 3400개, 상장 폐지된 회사 또는 기타 법인을 포함하는 듯 함)
# 다시 정리한 데이터의 고유번호를 이용하여 각 회사의 기업 개황정보를 요청
# 요청한 자료를 딕슈너리와 리스트에 담아 그대로 저장

######################################################################
# 인증키는 반드시 별도로 보관하고, 실수로 소스코드에 저장하지 않도록 주의
# 아래 '        ' 안에 개인 인증키 입력하여 소스 실행
CRTFC_KEY = '        '
######################################################################

import requests # 사용이 편리한 HTTP 라이브러리

url = 'https://opendart.fss.or.kr/api/corpCode.xml' # 데이터가 위치한 곳
params = { 'crtfc_key' : CRTFC_KEY} # 인증키는 반드시 별도로 보관하고, 실수로 소스코드에 담지 않도록 주의
# 인증키, 인증키는 일반적으로 파일을 분리하여 따로 저장하고 공유하지 않음

resp = requests.get(url, params=params ) # GET 요청, 파라미터를 딕슈너리로 다룸


# 오픈다트에서 공시목록 정보 중 고유번호 API는
# Zip 파일을 binary로 제공하기 때문에 처리할 게 많음
# 필요한 클래스들을 임포트 하여 처리
from io import BytesIO
from zipfile import ZipFile

# 받은 응답의 내용물을 인메모리 바이트버퍼를 이용하는 바이너리스트림으로
# 그걸 다시 ZipFile로 모두 추출하여 현재 디렉토리에 저장
import os # 리눅스와 윈도우는 경로 지정 문자가 다르므로 일관된 처리 필요
with ZipFile(BytesIO(resp.content)) as zip :
    cwd = os.getcwd()  # 현재 작업 디렉토리(Current Working Directory)
    zip.extractall(cwd) # 운영체제 상관 없이 현재 작업 디렉토리에 파일 생성
# 여기까지 완료하면 Zip 파일 안에 담긴 CORPCODE.xml 파일이 나타남


# 위에서 추출한 CORPCODE.xml 파일을 파싱하고
# 파이썬에서 활용 가능한 자료구조에 담기
# 각 회사 정보는 딕슈너리에 담고, 그 딕슈너리는 리스트에 담기
from xml.etree.ElementTree import parse
xml_tree = parse('./CORPCODE.xml')
xml_root = xml_tree.getroot()
xml_list = xml_root.findall('list')

comp_list = []  # 회사 정보 딕슈너리들을 모아 담을 리스트

for comp in xml_list:
    corp_code = comp.findtext('corp_code')
    corp_name = comp.findtext('corp_name')
    stock_code = comp.findtext('stock_code') 
    # 여기서 stock_code는 문자열 자료인데, 
    # ' '로 표시된 회사들은 비상장회사
    modify_date = comp.findtext('modify_date')
    comp = {    # 각 회사 정보는 딕슈너리에 저장
        'corp_code' : corp_code, 
        'corp_name' : corp_name, 
        'stock_code' : stock_code, 
        'modify_date' : modify_date 
    }
    comp_list.append(comp)

print(f'The length of comp_list : {len(comp_list)}') 
# 89398, 9만개에 가까운 데이터들, '삼화당피앤티'는 고유번호가 같은 게 2개가 있는데?


# 데이터가 너무 많아 상장 종목 코드를 가진 기업 정보만 살펴보기 위해 일부만 추출
# 개인 이용자는 오픈다트에 하루 API 요청 1만번만 가능하기 때문에 
# 9만 개의 데이터 모두를 하루에 요청할 수 없기 때문
listed_comp_list = []

for comp in comp_list:
    check = comp['stock_code']
    if (check.isspace() == False) and (check != ''):
        # 종목코드가 비어있지 않으면 일단 수집 
        listed_comp_list.append(comp)

print(f'The length of listed_comp_list : {len(listed_comp_list)}') 
# 약 9만개의 기업 중 약 3400개 회사가 남았음, 이중에서
# 상장 회사는 약 2천개이므로 상장폐지나 기타 법인이 섞여 있을 것으로 추측
# 그래도 일단 변수 이름은 listed_comp_list


# 기업 개황 정보를 요청
# 위 9만개 기업 중 추출한 3400개 기업의 기업 개황 정보
# 오픈다트에 API 요청
url = 'https://opendart.fss.or.kr/api/company.json' 

comp_profile_list = []  # 기업별 기업 개황정보들을 담을 리스트

num = 0
for comp in listed_comp_list: # 약 3400개의 API 요청
    # 선행 0이 숫자로 오해받지 않도록 값은 문자열 상태를 유지
    corp_code = comp['corp_code']
    
    params = { 
        'crtfc_key': CRTFC_KEY, # 인증키는 반드시 별도로 보관하고, 실수로 소스코드에 담지 않도록 주의
        'corp_code' : corp_code 
    }
    resp = requests.get(url, params)
    num +=1 # 몇 번째 요청이었는지
    print(f'{num:06} calling corp_code({corp_code})') # API 요청 상황

    if resp.status_code == 200:
        # 바이너리 Zip파일과 달리 이번에는 JSON 형태의 데이터
        comp_profile = resp.json() # JSON을 딕슈너리에 담기
        # JSON을 딕슈너리에 담은 후, 딕슈너리를 리스트에 추가하여 모으기
        comp_profile_list.append(comp_profile)
    

# 파이썬 자료구조를 그대로 파일로 저장
# 저장된 파일 comp_profile_list.p는 파이썬으로 불러와야만 다시 사용 가능
# pickle이라는 이름 처럼피클을 담고, 나중에 그대로 불러오기
import pickle

with open('comp_profile_list.p', 'wb') as f :
    pickle.dump(comp_profile_list, f)
