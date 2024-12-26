import time

from settings.log_setup import general_logger, exception_logger

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SearchProduct:
    def __init__(self, driver):
        self.driver = driver
        self.search_bar_xpath = '/html/body/header/nav/div[3]'
        self.input_box_xpath = '//*[@id="autocompleteInput"]'
        self.search_result_xpath = '/html/body/header/nav/div[3]/div/div/div[2]/div/ul/div/div/div/a/p[1]'
        self.product_page_xpath = '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[1]/h1'

    def open_search_bar(self):
        try:
            search_bar = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.search_bar_xpath))
            )
            search_bar.click()
            general_logger.info("SearchBar clicked successfully")
        except Exception as e:
            exception_logger.error(f"Error opening search bar: {e}")
            return False
        return True
    
    def enter_search_query(self, product_name):
        try:
            text_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.input_box_xpath))
            )
            text_input.clear()
            text_input.send_keys(product_name)
            general_logger.info("Search query entered successfully")
        except Exception as e:
            exception_logger.error(f"Error entering product name in search bar: {e}")
            return False
        return True

    def fetch_and_click_product(self):
        try:
            product = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.search_result_xpath))
            )
            product_name = product.text
            product.click()
            general_logger.info(f"Fetched Product Name: {product_name}")
            return product_name
        except Exception as e:
            exception_logger.error(f"Error fetching or clicking on product: {e}")
            return None

    def validate_product_page(self, expected_url):
        try:
            time.sleep(5)  # Allow the product page to load
            actual_url = self.driver.current_url
            if actual_url == expected_url:
                return True
        except Exception as e:
            exception_logger.error(f"Error validating product page: {e}")
        return False

    def get_product_name(self):
        try:
            product_name = self.driver.find_element(By.XPATH, self.product_page_xpath).text
            general_logger.info("Search query en")
            return product_name
        except Exception as e:
            exception_logger.error(f"Error fetching product name from product page: {e}")
            return None