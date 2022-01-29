<파이썬으로 QR code 생성 및 vCard 만들기>

1. 패키지 설치
pip install qrcode[pil]

2. vCard 포맷에 맞게 문자열 작성
BEGIN:VCARD
VERSION:3.0
N:산책;김;;;
FN:김산책
TITLE:산책왕
ORG:동네마실팀
URL:https://동네마실팀홈페이지
TEL:010-0000-0000
EMAIL:산책왕@동네마실팀이메일
ADR:대한민국
END:VCARD 

3. QR code 생성하여 이미지로 저장