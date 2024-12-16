from settings.config import WebDriverSetup, logger

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

def addProductfromSearchbar():
    # Create WebDriverSetup instance
    web_driver_setup = WebDriverSetup(headless=False)  # or True for headless mode

    driver = web_driver_setup.setup_driver()

    driver.get("https://nourishstore.in/")
    
    search_bar_click = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/header/nav/div[3]'))
    )
    search_bar_click.click()

    time.sleep(5)

    text_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="autocompleteInput"]'))
    )
    text_input.send_keys('arhar')

    fetch_product_text = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/header/nav/div[3]/div/div/div[2]/div/ul/div/div/div/a/p[1]'))
    )
    logger.info(fetch_product_text.text)
    logger.info('Search bar clicked')
    
    web_driver_setup.close_driver()

if __name__ == "__main__":
    addProductfromSearchbar()
    
'''
inspite of using time.sleep now and then after every element. whta other option dpo i have

def addProductfromSearchbar():
    # Create WebDriverSetup instance
    web_driver_setup = WebDriverSetup(headless=False)  # or True for headless mode
    
    # Get WebDriver
    driver = web_driver_setup.setup_driver()

    driver.get("https://nourishstore.in/")

    # Wait until the search bar is clickable and click it
    search_bar_click = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/header/nav/div[3]'))
    )
    search_bar_click.click()
    
    # Wait until the text input is visible and send 'arhar' text
    text_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="autocompleteInput"]'))
    )
    text_input.send_keys('arhar')
    
    # Wait for the product text to become visible
    fetch_product_text = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/header/nav/div[3]/div/div/div[2]/div/ul/div/div/div/a/p[1]'))
    )
    print(fetch_product_text.text)

    # Log message after the search bar is clicked
    logger.info('Search bar clicked')

    # Close the driver when done
    web_driver_setup.close_driver()
'''