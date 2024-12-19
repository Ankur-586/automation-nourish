from settings.config import WebDriverSetup
from settings.log_setup import general_logger, exception_logger

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

def addProductfromSearchbar():
    try:
        web_driver_setup = WebDriverSetup(headless=True)  # Change to True for headless mode
        driver = web_driver_setup.setup_driver()
        general_logger.info("WebDriver initialized successfully.")
    except Exception as e:
        exception_logger.error(f"Error initializing WebDriver: {e}")
        return

    # Open the website
    try:
        driver.get("https://nourishstore.in/")
        general_logger.info("Navigated to nourishstore.in.")
    except Exception as e:
        exception_logger.error(f"Error loading website: {e}")
        driver.quit()
        return

    # Click on the search bar
    try:
        search_bar_click = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/header/nav/div[3]'))
        )
        search_bar_click.click()
        general_logger.info("Search bar clicked.")
    except Exception as e:
        exception_logger.error(f"Search Bar Exception: {e}")
        driver.quit()
        return

    time.sleep(5)  # It's good to avoid hard waits, but leaving it here temporarily for testing purposes.

    # Input the search query
    try:
        text_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="autocompleteInput"]'))
        )
        text_input.send_keys('arhar')
        general_logger.info("Search term 'arhar' entered in the search bar.")
    except Exception as e:
        exception_logger.error(f"Error entering text in the search bar: {e}")
        driver.quit()
        return

    # Fetch product name from search results
    try:
        fetch_product_text = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/header/nav/div[3]/div/div/div[2]/div/ul/div/div/div/a/p[1]'))
        )
        general_logger.info(f"Fetched product: {fetch_product_text.text}")
    except Exception as e:
        exception_logger.error(f"Error fetching product text: {e}")
        driver.quit()
        return

    # Log that everything was successful
    general_logger.info("Product search from search bar completed successfully.")

    
    web_driver_setup.close_driver()

if __name__ == "__main__":
    addProductfromSearchbar()
    
'''
presence_of_element_located

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