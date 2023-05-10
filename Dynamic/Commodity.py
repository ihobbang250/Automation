from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd
from collections import defaultdict

# Setting Option
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging']) # Usb Error ignore
options.add_argument("no-sandbox") 
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("headless")

# Option Control to Speed up
prefs = {'profile.default_content_setting_values': {'cookies' : 1, 'images': 2, 'plugins' : 2, 'popups': 2, 
                                                    'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 
                                                    'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 
                                                    'media_stream_mic' : 2, 'media_stream_camera': 2, 
                                                    'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 
                                                    'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 
                                                    'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}   
options.add_experimental_option('prefs', prefs)


browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

CATECORY = ['agriculture', 'energy', 'metals']
data = defaultdict(list)

for category in CATECORY:
    browser.get("https://www.reuters.com/markets/commodities/" + category + "/news")

    print("---------")
    print(category)
    print("---------")

    #Load more articles
    button = browser.find_element(By.CSS_SELECTOR, "button[data-testid=Button] span[data-testid=Text]")
    button.click()
    time.sleep(2)

    #Scraping Headlines
    headlines= browser.find_elements(By.CSS_SELECTOR, "a[data-testid=Heading]")
    for heading in headlines:
        data[category].append(heading.text)
    
    print(len(data[category]))

### Data length difference -> Need to length uniform
## ex) agri -> 29 energy -> 25
min_length = min(len(lst) for lst in data.values())
trimmed_data = {key: lst[:min_length] for key, lst in data.items()}
df = pd.DataFrame(trimmed_data)
df.to_csv("NEWS_data.csv", index = False)