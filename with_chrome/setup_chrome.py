import json
from requests.structures import CaseInsensitiveDict

# https://github.com/SeleniumHQ/selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# https://github.com/SergeyPirogov/webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager

from settings.log_setup import general_logger, exception_logger

from fake_useragent import UserAgent

class WebDriverSetup:
    
    def __init__(self, headless=True, ignore_cert_errors=True, user_agent=None):
        self.headless = headless
        self.ignore_cert_errors = ignore_cert_errors
        self.user_agent = user_agent or self.get_random_user_agent()
        self.driver = None
        
    def get_random_user_agent(self):
        try:
            ua = UserAgent()
            return ua.random
        except Exception as e:
            exception_logger.error(f"Error generating User-Agent: {e}")
            
    def setup_driver(self):
        chrome_options = webdriver.ChromeOptions()
        
        chrome_options.add_argument(f'--user-agent={self.user_agent}')
        
        # Headless mode
        if self.headless:
            chrome_options.add_argument("--headless=new")
            
        # Ignore certificate errors
        if self.ignore_cert_errors:
            chrome_options.add_argument("ignore-certificate-errors")
        
        # Set window size
        chrome_options.add_argument("start-maximized")
        
        # Initialize WebDriver
        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                           options=chrome_options)
            general_logger.info(f"WebDriver setup complete with User-Agent: {self.user_agent}")
        except Exception as e:
            exception_logger.error(f"{e}")
            raise
        
        return self.driver
    
    def close_driver(self):
        if self.driver:
            self.driver.quit()
            general_logger.info("WebDriver closed successfully.")
        else:
            exception_logger.error("WebDriver was not initialized.")