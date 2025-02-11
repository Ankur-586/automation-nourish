import json
from requests.structures import CaseInsensitiveDict

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from fake_useragent import UserAgent

ua = UserAgent()
users_agent = ua.random
url = 'https://nourishstore.in/'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-agent={users_agent}")
chrome_options.add_argument("--headless=new")
chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options
        )
driver.get(url)
responses = []
response = None
for log_entry in driver.get_log("performance"):
    log_message = json.loads(log_entry["message"])["message"]
    # Filter out HTTP responses
    if log_message["method"] == "Network.responseReceived":
        responses.append(log_message["params"]["response"])
        if log_message["params"]["type"] == "Document":
            response = log_message["params"]["response"]
# print(response)
# headers = CaseInsensitiveDict(response["headers"])
status_code = response["status"]
print(f"HTTP Status code: {status_code}")
# print(f"Headers: {headers}")