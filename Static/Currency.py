# requests -> text 데이터 받아와 원하는 문자열 추출
# naver 환율 페이지 활용 간단한 환율조회 및 달러 환율 계산
import requests as req
import re

res = req.get("https://finance.naver.com/marketindex/?tabSel=exchange#tab_section")

body = res.text

# Use RegEx to extract the text
r = re.compile(r"h_lst.*?blind\">(.*?)</span>.*?value\">(.*?)</", re.DOTALL)
captures = r.findall(body)

print("--------------------------------")
print("전체환율조회")
print("--------------------------------")

for c in captures:
    print(f"{c[0]} : {c[1]}원")

print("--------------------------------")
print("원화/달러 계산")
print("--------------------------------")
usd = float(captures[0][1].replace(",", ""))
won = int(input("달러로 바꾸길 원하는 금액(원) 입력해주세요: "))
dollar = round((won / usd), 1)
print(f"{won}원 -> {dollar}달러")