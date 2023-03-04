from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyperclip
import pyautogui
import os
from dotenv import load_dotenv

# Setting User Data at System variables
# Create .env file in the same directory as this script
load_dotenv()
DATA = {"id":os.getenv("NAVER_ID"), "pw":os.getenv("NAVER_PW")}

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging']) # Usb Error ignore
options.add_argument("no-sandbox") 

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
browser.get("https://shopping.naver.com")

wait = WebDriverWait(browser, 10)

# Presence method detail version -> visibility
# Visibility method
def find(wait, css_selector):
    return wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))

# Auto input method
def auto_input(type):
    input_data = find(wait, f"input#{type}")
    input_data.click()
    pyperclip.copy(DATA[type])
    # pyautogui.hotkey('ctrl', 'v') # window version
    pyautogui.keyDown('command') # mac version
    pyautogui.press('v')
    pyautogui.keyUp('command')
    if type == "id":
        time.sleep(1)
    else:
        input_data.send_keys("\n")

# Login process
login_button = find(wait, "a#gnb_login_button")
login_button.click()
auto_input("id")
auto_input("pw")

# Logout Process
# logout_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a#gnb_logout_button")))
# logout_button.click()
# time.sleep(3)

search = find(wait, "form[name=search] input[type=text]")
search.click()
search.send_keys("갤럭시Z플립3 케이스")
time.sleep(1)
search.send_keys("\n")

# Wait for loading
find(wait, "div[class^=basicList_info]")
# Scroll to bottom
for i in range(8):
    browser.execute_script("window.scrollBy(0, 10000)")
    time.sleep(1)
# Print item list
items = browser.find_elements(By.CSS_SELECTOR, "div[class^=basicList_title]")
for item in items:
    # Remove ADs
    try:
        item.find_element(By.CSS_SELECTOR, "button[class^=ad_]")
        continue
    except:
        pass
    print(item.text)

find(wait, "a[class^=basicList_link]").click()
time.sleep(2)

# Browser switch to new tab
browser.switch_to.window(browser.window_handles[1])
print(browser.title)

browser.close()