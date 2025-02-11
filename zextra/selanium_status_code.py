import json
from requests.structures import CaseInsensitiveDict

# https://github.com/SeleniumHQ/selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# https://github.com/SergeyPirogov/webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager


class ChromeWebDriverPerfomance:
    def __init__(self, headless=False):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--headless=new")
        self.options.add_argument("disable-infobars")
        self.options.add_argument("--disable-extensions")
        # https://developer.chrome.com/docs/chromedriver/logging/performance-log
        self.options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=self.options
        )

        # List to store each response
        self.responses = []

    def get(self, url):
        self.driver.get(url)

        # Parse the Chrome Performance logs
        response = None
        for log_entry in self.driver.get_log("performance"):
            log_message = json.loads(log_entry["message"])["message"]
            # Filter out HTTP responses
            if log_message["method"] == "Network.responseReceived":
                self.responses.append(log_message["params"]["response"])
                if log_message["params"]["type"] == "Document":
                    response = log_message["params"]["response"]
        return response

    def close(self):
        self.driver.close()


if __name__ == "__main__":
    start_url = "https://nourishstore.in/"
    cwd_perf = ChromeWebDriverPerfomance()
    response = cwd_perf.get(start_url)
    cwd_perf.close()

    """
    The ChromeWebDriver response attribute(s) contain a dict with information about the response
    {
        "connectionId": [Integer],
        "connectionReused": [Boolean],
        "encodedDataLength": [Integer],
        "fromDiskCache": [Boolean],
        "fromServiceWorker": [Boolean],
        "headers": [dict], # HTTP Headers as a dict
        "headersText": [String], # HTTP Headers as text
        "mimeType": [String],
        "protocol": [String],
        "remoteIPAddress": [String],
        "remotePort": [Integer],
        "requestHeaders": [dict],
        "requestHeadersText": [String],
        "securityDetails": [dict], # TLS/SSL related information
        "securityState": [String],
        "status": [Integer], # HTTP Status Code of the Response
        "statusText": [String],
        "timing": [dict],
        "url": [String]
    }
    """
    headers = CaseInsensitiveDict(response["headers"])
    status_code = response["status"]
    print(f"HTTP Status code: {status_code}")
    print(f"Headers: {headers}")
    
# ----------------------------------------------------
# selenium get status code python 
# https://gist.github.com/LeMoussel/bfed69044cb65947a4e63c76f11e6e1f#file-chromedriver_get_response-py-L14