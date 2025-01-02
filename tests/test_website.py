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

def test_open_site(driver_setup):
    
    driver = driver_setup
    try:
        driver.get("https://nourishstore.in/")
        general_logger.info("Navigated to nourishstore.in")
    except Exception as e:
        exception_logger.error(f"Error loading website: {e}")
        pytest.fail(f"Failed to load website: {e}")
        driver.close()
        
def test_add_product(driver_setup):
    """
    Test case for adding a product from the search bar to the cart.
    """
    driver = driver_setup
    driver.get("https://nourishstore.in/")
    search_page = SearchProduct(driver)

    product_name = "Nourish Nutrition Delights Combo of 3"  # Use a product name for the test

    # Perform search and selection
    assert search_page.open_search_bar(), "Failed to open search bar"
    assert search_page.enter_search_query(product_name), "Failed to enter search query"
    product_name_from_search = search_page.fetch_and_click_product()

    assert product_name_from_search, "Failed to fetch or click on product"

    # Validate the product page
    expected_product_page_url = "https://nourishstore.in/offers/nourish-nutrition-delights-combo-of-3"
    assert search_page.validate_product_page(expected_product_page_url), "Product page did not open successfully"

    # Get the product name and prices
    product_name_from_page = search_page.get_product_name()
    assert product_name_from_page == product_name_from_search, "Product name mismatch"

    # Get product prices for different weights
    prices = search_page.add_product_to_cart()
    assert prices, "Failed to fetch product prices"

    # If you want to log the prices, you can do so here
    general_logger.info(f"Prices: {prices}")
    driver.quit()
    # # Create an instance of the SearchPage class with the driver passed to it
    # search_page = SearchProduct(driver)

    # # Perform actions using the SearchPage class
    # if not search_page.open_search_bar():
    #     assert 
    # if not search_page.enter_search_query(product_name):
    #     return

    # # Fetch the product and click it
    # product_name_from_search = search_page.fetch_and_click_product()
    # if not product_name_from_search:
    #     return

    # # Validate that the correct product page has opened
    # expected_product_page_url = 'https://nourishstore.in/unpolished-dal/arhar-dal'
    # if search_page.validate_product_page(expected_product_page_url):
    #     general_logger.info("Product page opened successfully.")
    # else:
    #     exception_logger.error("Product page did not open successfully.")
    #     return

    # # Get the product name from the product page
    # product_name_from_page = search_page.get_product_name()
    # if product_name_from_page:
    #     general_logger.info(f"Product name on product page: {product_name_from_page}")
    # else:
    #     exception_logger.error("Error fetching product name from product page.")

    # # get actual price of 500 gm product
    # product_weight = search_page.get_weight_dropDown()
    # if actual_500_gm_product_price:
    #     general_logger.info(f"Actual 500 gm product price: ₹{actual_500_gm_product_price}")
    # else:
    #     return
        
    # Close the WebDriver
# x = driver_setup
# x.close_driver()

# AddProductFromSearchbar('arhar')

