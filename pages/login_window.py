import time

from settings.log_setup import general_logger, exception_logger

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class LoginWindow:
    def __init__(self, driver):
        self.driver = driver
        self.loginWindow = '.align-bottom svg' 
    
    def login_window(self):
        try:
            login_window = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.loginWindow))
            )
            login_window.click()
            general_logger.info("Login Pop Up Window Click")
            return True
        except Exception as e:
            exception_logger.error(f"Error opening Login Pop Up Window Click {e}")