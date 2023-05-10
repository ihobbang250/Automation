from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Setting Option
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging']) # Usb Error ignore
options.add_argument("no-sandbox") 
options.add_argument("disable-gpu") 
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

for category in CATECORY:
    browser.get("https://www.reuters.com/markets/commodities/" + category + "/news")
    #wait = WebDriverWait(browser, 10)
    print("---------")
    print(category)
    print("---------")
    
    #Load more articles
    button = browser.find_element(By.CSS_SELECTOR, "button[data-testid=Button] span[data-testid=Text]")
    button.click()

    #Scraping Headlines
    headlines= browser.find_elements(By.CSS_SELECTOR, "a[data-testid=Heading]")
    for heading in headlines:
        print(heading.text)
