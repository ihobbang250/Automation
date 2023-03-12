# Auto Customize PC

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

options = webdriver.ChromeOptions() 
options.add_experimental_option('excludeSwitches', ['enable-logging']) # Usb Error ignore
options.add_argument("no-sandbox") 
options.add_argument("headless")

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
browser.get("https://shop.danawa.com/virtualestimate/?controller=estimateMain&methods=index&marketPlaceSeq=16")

wait = WebDriverWait(browser, 10)

FILTER_OPTIONS = {
    "Mainboard_SOCKET": 2,
    "Memory_SOCKET": 2,
    "Memory_SIZE": 3,
    "SSD_SIZE": 4,
    "Case_SIZE": 2,
    "Power_SIZE": 2
}

CATEGORY = {
    "CPU": "873",
    "Cooler": "887",
    "Mainboard": "875",
    "Memory": "874",
    "GPU": "876",
    "SSD": "32617",
    "Case": "879",
    "Power": "880"
}

CATERGORY_CSS = {
    c: "dd.category_" + CATEGORY[c] + " a" for c in CATEGORY
}

user_cart = {}

def find_visible(css):
    return wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css)))


def find_visibles(css):
    """
    Find all include selector
    """
     
    find_visible(css)
    return browser.find_elements(By.CSS_SELECTOR, css)


def text_deco(text):
    print("--------------------------------")
    print(text)
    print("--------------------------------")


def condition_count(part, options):
    keys = []
    for key in options.keys():
        if part in key:
            keys.append(key)
    return keys
        

def auto_select(part, dependency=None):
    find_visible(CATERGORY_CSS[part]).click()
    time.sleep(1)
    options = find_visibles("div.search_option_item")
    for option in condition_count(part, FILTER_OPTIONS):    
        row = FILTER_OPTIONS[option]
        options[row].find_elements(By.CSS_SELECTOR, "button")[0].click()
        checkboxs = find_visibles("div[class$=open] span.item_text")
        if "SIZE" in option:
            print(f"{part} 선택")
            for idx, item in enumerate(checkboxs):
                print(f"{idx+1}: {item.text.strip()}")
            num = int(input())
            select_item = checkboxs[num-1]
            select_item.click()
            time.sleep(1)
        
        if dependency is not None:        
            for s in checkboxs:
                if s.text.strip() in dependency:
                    s.click()
                    if len(condition_count(part, FILTER_OPTIONS)) != 0:
                        options[row].find_elements(By.CSS_SELECTOR, "button")[0].click()
                    time.sleep(1)
                    break
    

def auto_select_list(part):
    products = find_visibles("div.scroll_box tr[class^=productList]")
    products_list = []
    for p in products:
        name = p.find_element(By.CSS_SELECTOR, "p.subject a").text
        #name = re.sub(r"\(.* ?\)", "", name).strip()
        try:
            price = p.find_element(By.CSS_SELECTOR, "span.prod_price").text
            price = int(re.sub(r'[^0-9]', "", price))
        except:
            continue
        if part == "Mainboard":
            spec = p.find_element(By.CSS_SELECTOR, "a.spec").text
            memory_slot = re.findall(r"DDR\d", spec)[0]
            products_list.append([name, memory_slot, price])
        else:
            products_list.append([name, price])
        if len(products_list) > 4:
            break
    user_cart[part] = products_list


# cpu category
cpu = find_visible(CATERGORY_CSS["CPU"])
cpu.click()
time.sleep(1)

# cpu company
options = find_visibles("input[name=makerCode]+span")
text_deco("CPU 제조사 번호를 선택")
for idx, o in enumerate(options):
    print(f"{idx+1}. {o.text}")
choice = int(input("-> "))
options[choice-1].click()
time.sleep(1)

# cpu list
products = find_visibles("div.scroll_box tr[class^=productList]")
products_list = []
text_deco("CPU를 선택")
for idx, p in enumerate(products):
    name = p.find_element(By.CSS_SELECTOR, "p.subject a").text
    name = re.sub(r"\(.* ?\)", "", name).strip()
    spec = p.find_element(By.CSS_SELECTOR, "a.spec").text
    socket = spec.split("/")[0]
    if name.find("AMD") != -1:
        core = int(re.findall(r'\d+', spec.split("/")[3])[0])
        thread = int(re.findall(r'\d+', spec.split("/")[4])[0])
        clock = float(re.findall(r'\d.\d', spec.split("/")[5].split(":")[1])[0])
        performance = int(core * thread * clock)
    else:
        core = re.findall(r'\d+', spec.split("/")[2])
        core = sum([int(x) for x in core])
        thread = re.findall(r'\d+', spec.split("/")[3])
        thread = sum([int(x) for x in thread])
        clock = float(re.findall(r'\d.\d', spec.split("/")[4].split(":")[1])[0])
        performance = int(core * thread * clock)
    try:
        price = p.find_element(By.CSS_SELECTOR, "span.prod_price").text
        price = int(re.sub(r'[^0-9]', "", price))
    except:
        price = None
    products_list.append([name, socket, price, performance])
    #print(f"{idx+1}. {name}/ {socket} / {price} / {performance}")
print("원하는 조합 방식을 선택")
print("1.인기 2.성능 3.가격")
choice = int(input("-> "))
if choice == 1:
    choice_popular_cpu = products_list[0]
elif choice == 2:
    choice_perform_cpu = sorted(products_list, key=lambda x: x[4])[0]
    print(choice_perform_cpu)
elif choice == 3:
    choice_price_cpu = sorted(products_list, key=lambda x: x[3], reverse=True)[0]
    print(choice_price_cpu)
else:
    raise Exception("Invalid choice")

selected_cpu = products_list[choice-1]
selected_socket = selected_cpu[1]
time.sleep(2)

# gpu category
gpu = find_visible(CATERGORY_CSS["GPU"])
gpu.click()
time.sleep(1)

# gpu list
products = find_visibles("div.scroll_box tr[class^=productList]")
products_list = []
text_deco("GPU를 선택")
for idx, p in enumerate(products):
    name = p.find_element(By.CSS_SELECTOR, "p.subject a").text
    name = re.sub(r"\(.* ?\)", "", name).strip()
    spec = p.find_element(By.CSS_SELECTOR, "a.spec").text
    try:
        price = p.find_element(By.CSS_SELECTOR, "span.prod_price").text
        price = int(re.sub(r'[^0-9]', "", price))
    except:
        price = None
    products_list.append([name, price])
    print(f"{idx+1}. {name}/ {price}")
choice = int(input("-> "))
selected_gpu = products_list[choice-1]

## Auto Select ##
auto_select("Mainboard", selected_socket)
auto_select_list("Mainboard")

# mainboard list
memory_socket = user_cart["Mainboard"][0][1]

# memory 
auto_select("Memory", memory_socket)
auto_select_list("Memory")

# ssd 
auto_select("SSD")
auto_select_list("SSD")

# case 
auto_select("Case")
auto_select_list("Case")

# power category
auto_select("Power")
auto_select_list("Power")

for key, item in user_cart.items():
    print(key, ":", item)

## Customize by price, popular ##
# Mainboard Memory Socket select issue
# Sol) When Customize, select Mainboard effects select Memory
# Call auto_select("Memory") again

user_cart["Mainboard"]

browser.quit()