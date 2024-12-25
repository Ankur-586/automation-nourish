from settings.config import WebDriverSetup

from settings.test import general_logger, exception_logger

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def AddProductFromSearchbar(product_name: str):
    
    try:
        if not isinstance(product_name, str):
            exception_logger.error("Product name should be a string")
            return
        # The rest of your function logic goes here
    except Exception as e:
        exception_logger.error(f"Error: {e}")

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
        return

    # time.sleep(5)  # It's good to avoid hard waits, but leaving it here temporarily for testing purposes.

    # # Input the search query
    # try:
    #     text_input = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, '//*[@id="autocompleteInput"]'))
    #     )
    #     text_input.send_keys(product_name)
    #     general_logger.info(f"Search term {product_name} entered in the search bar.")
    # except Exception as e:
    #     log_exception(f"Error entering text in the search bar: {e}")
    #     return

    # # Fetch product name from search results
    # try:
    #     fetch_product_text = WebDriverWait(driver, 10).until(
    #         EC.visibility_of_element_located((By.XPATH, '/html/body/header/nav/div[3]/div/div/div[2]/div/ul/div/div/div/a/p[1]'))
    #     )
    #     general_logger.info(f"Fetched product: {fetch_product_text.text}")
    # except Exception as e:
    #     log_exception(f"Error fetching product text: {e}")
    #     return
    
    # # Click on the product to open the product page
    # try:
    #     fetch_product_text.click()
    #     time.sleep(5)
    #     expected_product_page_url = 'https://nourishstore.in/unpolished-dal/arhar-dal'
    #     actual_product_page_url = driver.current_url
    #     if expected_product_page_url == actual_product_page_url:
    #         general_logger.info("Product page opened successfully")
    #         return 'Pass'
    #     log_exception("Product page did not open successfully")
    #     return 'Fail'
    # except Exception as e:
    #     log_exception(f"Error opening product page: {e}")
    
    # try:
    #     product_name = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[1]/h1')
    #     general_logger.info(f"Product name: {product_name}")
    # except Exception as e:
    #     log_exception(f"Error fetching product name: {e}")
    
    # # Log that everything was successful
    # general_logger.info("Product search from search bar completed successfully.")

    # web_driver_setup.close_driver()

if __name__ == "__main__":
    AddProductFromSearchbar(56)
    
