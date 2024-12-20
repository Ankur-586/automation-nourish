from settings.config import WebDriverSetup
from settings.log_setup import general_logger, exception_logger

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

def AddProductFromSearchbar(product_name: str):
    if isinstance(product_name, str) is False:
        exception_logger.error("Product name should be a string.")
        return

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
        text_input.send_keys(product_name)
        general_logger.info(f"Search term {product_name} entered in the search bar.")
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
    
    # Click on the product to open the product page
    try:
        fetch_product_text.click()
        time.sleep(5)
        expected_product_page_url = 'https://nourishstore.in/unpolished-dal/arhar-dal'
        actual_product_page_url = driver.current_url
        if expected_product_page_url == actual_product_page_url:
            general_logger.info("Product page opened successfully")
        else:
            exception_logger.error("Product page did not open successfully")
    except Exception as e:
        exception_logger.error(f"Error opening product page: {e}")
    
    # Log that everything was successful
    general_logger.info("Product search from search bar completed successfully.")

    web_driver_setup.close_driver()

if __name__ == "__main__":
    AddProductFromSearchbar(69)
    
