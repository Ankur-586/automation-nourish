import time

from settings.log_setup import general_logger, exception_logger

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class SearchProduct:
    def __init__(self, driver):
        self.driver = driver
        self.search_bar_xpath = '/html/body/header/nav/div[3]'
        self.input_box_xpath = '//*[@id="autocompleteInput"]'
        self.search_result_xpath = '/html/body/header/nav/div[3]/div/div/div[2]/div/ul/div/div/div/a/p[1]'
        self.product_page_xpath = '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[1]/h1'
        self.select_weight_dropdown = '//*[@id="select1"]'
        self.actualPrice_product = '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span[2]'
        self.discountedPrice_product = '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span[1]'
        self.add_to_cart = '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/button'

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
            general_logger.info(f"Fetched Product Name from search bar: {product_name}")
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
            return product_name
        except Exception as e:
            exception_logger.error(f"Error fetching product name from product page: {e}")
            return None
        
    def get_weight_dropDown(self):
        try:
            select = Select(self.driver.find_element(By.XPATH, self.select_weight_dropdown))
            for idx in range(select.options):
                select.select_by_index(idx)
                actul_product_price = self.driver.find_element(By.XPATH, self.select_weight_dropdown).text
            return actul_product_price
        except Exception as e:
            exception_logger.error(f"Error fetching product price from product page: {e}")
            return None
    # How to handle dropdown in Selenium Python?