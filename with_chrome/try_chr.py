from selenium.webdriver.chrome.service import Service
from selenium import webdriver

from with_chrome.setup_chrome import WebDriverSetup

import json

from fake_useragent import UserAgent

ua = UserAgent()

url = 'https://nourishstore.in/'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-agent={ua}")
chrome_options.add_argument("--headless=new")


web_driver_setup = WebDriverSetup(headless=True)
driver = web_driver_setup.setup_driver()


status_code_driver = driver.get(url)

# Parse the Chrome Performance logs
responses = []
response = None
for log_entry in status_code_driver.get_log("performance"):
    log_message = json.loads(log_entry["message"])["message"]
    # Filter out HTTP responses
    if log_message["method"] == "Network.responseReceived":
        responses.append(log_message["params"]["response"])
        if log_message["params"]["type"] == "Document":
            response = log_message["params"]["response"]
print(response)