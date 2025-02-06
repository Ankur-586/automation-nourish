# import os
# import sys
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# sys.path.insert(0, project_root)

from settings.config import WebDriverSetup
from settings.log_setup import general_logger, exception_logger

from pages.searchProd import SearchProduct

import pytest

@pytest.fixture()
def driver_setup():
    """
    This fixture sets up the WebDriver and performs product search actions.
    """
    web_driver_setup = WebDriverSetup(headless=True)  # Change to True for headless mode
    driver = web_driver_setup.setup_driver()
    yield driver  
    driver.quit()

def test_open_site(driver_setup):
    
    driver = driver_setup
    try:
        driver.get("https://nourishstore.in/")
        general_logger.info("Navigated to nourishstore.in")
    except Exception as e:
        exception_logger.error(f"Error loading website: {e}")
        pytest.fail(f"Failed to load website: {e}")
        
def test_add_product(driver_setup):
    """
    Test case for adding a product from the search bar to the cart.
    """
    driver = driver_setup
    driver.get("https://nourishstore.in/")
    search_page = SearchProduct(driver)

    # driver.implicitly_wait(10)
    
    product_name = "Kalonji".strip()  # Use a product name for the test

    # Perform search and selection
    assert search_page.open_search_bar() is True, "Failed to open search bar"
    assert search_page.enter_search_query(product_name) is True, "Failed to enter search query"
    
    product_name_from_search = search_page.fetch_and_click_product(product_name)

    assert product_name_from_search, "Failed to fetch or click on product"

    # Get the product name and prices
    product_name_from_page = search_page.get_product_name()
    assert product_name_from_page == product_name_from_search, "Product name mismatch"

    # Get product prices for different weights
    prices = search_page.add_product_to_cart(product_name_from_page)
    assert prices, "Failed to fetch product prices"

    



