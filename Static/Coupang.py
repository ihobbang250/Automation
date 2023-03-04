# Coupang Researcher
# Simple Version
import requests as req
from bs4 import BeautifulSoup as BS

url = "https://www.coupang.com/np/search?component=&q=%EB%85%B8%ED%8A%B8%EB%B6%81&channel=user"

# Use header information to avoid bot blocking
header = {
    'Referer': 'https://www.google.com/',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ko,th;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6,ko-KR;q=0.5,la;q=0.4',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
}
res = req.get(url,headers=header)
soup = BS(res.text, "html.parser")

# Remove ADs
for desc in soup.select("div.descriptions-inner"):
    ads = desc.select("span.ad-badge")
    if len(ads) != 0:
        print("광고")
    else:    
        print(desc.select("div.name")[0].get_text(strip=True))