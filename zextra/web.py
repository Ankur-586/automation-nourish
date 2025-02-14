import json, time
from requests.structures import CaseInsensitiveDict
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from fake_useragent import UserAgent

ua = UserAgent()
users_agent = ua.random
url = 'https://nourishstore.in/oil-ghee/mustard-oil'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-agent={users_agent}")
chrome_options.add_argument("--headless=new")
# chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
chrome_options.add_argument("start-maximized")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options
        )
driver.get(url)

add_to_cart = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/button')
for _ in range(10):
    add_to_cart.click()
    time.sleep(0.5)
    print('added')
cart_icon_click = driver.find_element(By.XPATH, '/html/body/header/nav/div[2]/div/div/div[2]/div[2]')
cart_icon_click.click()
time.sleep(5)
# C:\Users\Leads\.cache\selenium\chromedriver\win64\131.0.6778.204\chromedriver.exe