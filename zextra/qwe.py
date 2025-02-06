from settings.config import WebDriverSetup
from settings.log_setup import general_logger, exception_logger

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

website_url = 'https://nourishstore.in/'
web_driver_setup = WebDriverSetup(headless=False)  # Change to True for headless mode
driver = web_driver_setup.setup_driver()
driver.get(website_url)
x = driver.find_element(By.CSS_SELECTOR, '.align-bottom svg')
x.click()
time.sleep(5)
pop_window = driver.find_element(By.XPATH, '/html/body/header/nav/div[4]/div[2]/div/div/div')
if pop_window:
    mobile_input_box = driver.find_element(By.XPATH, '/html/body/header/nav/div[4]/div[2]/div/div/div/div/div[2]/div/div[2]/form/input')
    mobile_input_box.send_keys('123')
    next_button = driver.find_element(By.XPATH, '/html/body/header/nav/div[4]/div[2]/div/div/div/div/div[2]/div/div[2]/form/button')
    next_button.click()
    time.sleep(5)