# compbook_2.py
# compbook_1.py를 먼저 실행하여 데이터를 comp_profile_list.p에 저장하였다면
# 위 파일에 저장한 리스트, 딕슈너리를 다시 그대로 불러와서 작업

import pickle # 피클로 파이썬 자료구조를 그대로 파일에 저장/불러오기 가능

with open('comp_profile_list.p', 'rb') as f:
    comp_profile_list = pickle.load(f)  # 피클로 저장했던 리스트 그대로 불러오기

# 이제 comp_profile_list에 코스피(Y), 코스닥(K), 코넥스(N), 기타 법인(E)
# 기업 개황정보들이 각각 딕슈너리에 담겨 리스트의 요소로 담겨 있음

import csv # csv 는 파이썬으로 CSV 파일 생성, 읽기 등을 도와주는 기본 모듈

key_to_hangul = { 
    # 데이터를 CSV 파일로 저장하기 전 응답키를 한국어로 변환하기 위한 딕슈너리
    'corp_code':'고유번호', # 오픈다트 설명과 달리 'corp_code'도 들어 있음
    'status':'API요청응답상태', 
    'message':'API요청응답메시지', 
    'corp_name':'정식명칭', 
    'corp_name_eng':'영문명칭',
    'stock_name':'기업명', 
    'stock_code':'종목코드', 
    'ceo_nm':'대표자명', 
    'corp_cls':'법인구분', 
    'jurir_no':'법인등록번호',
    'bizr_no':'사업자등록번호',
    'adres':'주소', 
    'hm_url':'홈페이지', 
    'ir_url':'IR홈페이지', 
    'phn_no':'전화번호', 
    'fax_no':'팩스번호', 
    'induty_code':'업종코드', 
    'est_dt':'설립일(YYYYMMDD)', 
    'acc_mt':'결산월(MM)'
}

# 알아보기 힘든 API 응답키를 한글로 변경
comp_profile_list_hangul = [] # 새로 기업 개황정보들을 담을 리스트
for comp in comp_profile_list:
    comp_hangul = {} # 한글 키로 기업 개황정보를 담을 딕슈너리
    for old_key in comp.keys():
        new_key = key_to_hangul[old_key] # 위 딕슈너리를 이용
        comp_hangul[new_key] = comp[old_key]
    comp_profile_list_hangul.append(comp_hangul)

# CSV 파일에 넣을 필드 이름을 변경된 한글 이름으로 설정
fieldnames = [
    '고유번호', 
    'API요청응답상태', 
    'API요청응답메시지', 
    '정식명칭', 
    '영문명칭',
    '기업명', 
    '종목코드', 
    '대표자명', 
    '법인구분', 
    '법인등록번호', 
    '사업자등록번호',
    '주소', 
    '홈페이지', 
    'IR홈페이지', 
    '전화번호', 
    '팩스번호', 
    '업종코드', 
    '설립일(YYYYMMDD)', 
    '결산월(MM)'
]

with open('compbook.csv', 'w', newline='') as csvf:
    writer = csv.DictWriter(csvf, fieldnames=fieldnames)
    writer.writeheader()

    for comp in comp_profile_list_hangul:
        if comp['법인구분']!='E':   # E(기타)제외,Y(유가),K(코스닥),N(코넥스)만
            writer.writerow(comp)

# 여기 까지가 CSV 파일 생성
# 생성된 CSV 파일을 VSCode로 열어보면, 
# 선행 0을 포함하여 데이터가 문자열로 잘 저장됨


# 그러나,저장된 CSV 파일을 구글 스프레드시트에서 열면 괜찮은데, 
# 윈도우즈 엑셀에서 불러오면 한글이 깨짐(한글 인코딩 방식이 다르기 때문)
# 이를 직접 해결하려면 번거로움
# (엑셀에서 데이터 - 외부데이터가져오기 - 텍스트 - 구분자 설정)

# 따라서 pandas와 openpyxl 설치 후, pandas를 이용하여
# compbook.csv 파일을 xlsx 엑셀 파일로 변환하여 저장

import pandas as pd # 보통 pandas의 별명으로 pd를 사용

csv_load = pd.read_csv('compbook.csv', dtype=str, encoding='euc-kr') 
# dtype=str로 데이터의 선행 0 보존

xlsx = pd.ExcelWriter('compbook.xlsx')
csv_load.to_excel(xlsx, index=False) # xlsx 파일로 변환
xlsx.save() # xlsx 파일 저장
