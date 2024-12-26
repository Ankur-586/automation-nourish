# import os
# import sys
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# sys.path.insert(0, project_root)

from settings.config import WebDriverSetup
from settings.log_setup import general_logger, exception_logger

from pages.test_WebFlow import SearchProduct

def AddProductFromSearchbar(product_name: str):
    if not isinstance(product_name, str):
        exception_logger.error("Product name should be a string")
        return

    try:
        # Initialize the WebDriver outside the SearchPage class
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

    # Create an instance of the SearchPage class with the driver passed to it
    search_page = SearchProduct(driver)

    # Perform actions using the SearchPage class
    if not search_page.open_search_bar():
        return
    if not search_page.enter_search_query(product_name):
        return

    # Fetch the product and click it
    product_name_from_search = search_page.fetch_and_click_product()
    if not product_name_from_search:
        return

    # Validate that the correct product page has opened
    expected_product_page_url = 'https://nourishstore.in/unpolished-dal/arhar-dal'
    if search_page.validate_product_page(expected_product_page_url):
        general_logger.info("Product page opened successfully.")
    else:
        exception_logger.error("Product page did not open successfully.")
        return

    # Get the product name from the product page
    product_name_from_page = search_page.get_product_name()
    if product_name_from_page:
        general_logger.info(f"Product name on product page: {product_name_from_page}")
    else:
        exception_logger.error("Error fetching product name from product page.")

    web_driver_setup.close_driver()

AddProductFromSearchbar('arhar')