import requests as req
from bs4 import BeautifulSoup as BS
from collections import defaultdict
import pandas as pd

data = defaultdict(list)
CATEGORY = ['oil', 'gold', 'copper']

for c in CATEGORY:

    print("--------------------------------")
    print(c)
    print("--------------------------------")

    for i in range(50):
        url = "http://ft.com/"+ c+"?page=" +str(i)

        res = req.get(url)

        soup = BS(res.text, "html.parser")

        headlines = soup.select("div[class=o-teaser__heading]")

        for headline in headlines:
            data[c].append(headline.get_text())

df = pd.DataFrame(data)
df.to_csv("NEWS_data2.csv", index=False)
