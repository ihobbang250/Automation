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

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

CATECORY = ['agriculture', 'energy', 'metals']

for category in CATECORY:
    browser.get("https://www.reuters.com/markets/commodities/" + category)
    wait = WebDriverWait(browser, 10)
    print("---------")
    print(category)
    print("---------")
    
    #Load more articles
    button = browser.find_element(By.CSS_SELECTOR, "button[data-testid=Button] span[data-testid=Text]")
    print(button.text)

    #Scraping Headlines
    headlines= browser.find_elements(By.CSS_SELECTOR, "a[data-testid=Heading]")
    for heading in headlines:
        print(heading.text)
