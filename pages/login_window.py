import time

from settings.log_setup import general_logger, exception_logger

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class LoginWindow:
    def __init__(self, driver):
        self.driver = driver
        self.loginWindow_button = '.align-bottom svg' 
        self.loginpopWindow = '/html/body/header/nav/div[4]/div[2]/div/div/div'
        self.mobile_input_box = '/html/body/header/nav/div[4]/div[2]/div/div/div/div/div[2]/div/div[2]/form/input'
        self.next_button = '/html/body/header/nav/div[4]/div[2]/div/div/div/div/div[2]/div/div[2]/form/button'
    
    def wait_for_element(self, by, locator, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, locator))
            )
        except Exception as e:
            exception_logger.error(f"Element {locator} not found: {e}")
            return None
    
    def open_login_window(self):
        try:
            login_window = self.wait_for_element(By.CSS_SELECTOR, self.loginWindow_button)
            login_window.click()
            general_logger.info("Login Pop Up Window Click")
            return True
        except Exception as e:
            exception_logger.error(f"Error opening Login Pop Up Window Click {e}")
            return False
    
    def get_login_window(self, input_field_mobile):
        try:
            login_window = self.wait_for_element(By.CSS_SELECTOR, self.loginWindow_button)
            login_window.click()
            pop_window = self.wait_for_element(By.XPATH, self.loginpopWindow)
            if pop_window:
                general_logger.info('Found The Login/SignUp Form')
                mobile_input_box = self.driver.find_element(By.XPATH, self.mobile_input_box)
                mobile_input_box.send_keys(input_field_mobile)
                next_button = self.driver.find_element(By.XPATH, self.next_button)
                if next_button.is_enabled() and next_button.is_displayed():
                    next_button.click()
                    general_logger.info("Next Button was clicked!")
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            exception_logger.error(f"Login Pop Up Window Not Found: {e}")
            return False