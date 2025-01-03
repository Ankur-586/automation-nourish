import time

from settings.log_setup import general_logger, exception_logger

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

class SearchProduct:
    def __init__(self, driver):
        self.driver = driver
        self.search_bar = '/html/body/header/nav/div[3]'
        self.input_box = '//*[@id="autocompleteInput"]'
        self.search_result = '/html/body/header/nav/div[3]/div/div/div[2]/div/ul/div/div/div/a/p[1]'
        self.product_page = '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[1]/h1'
        self.multiple_weight_dropdown = '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/select'
        self.single_weight_nodropdown = '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/span'
        self.actualPrice_product = '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span[2]'
        self.discountedPrice_product = '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span[1]'
        self.add_to_cart = '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/button'
        # self.open_cart_with_product = ''

    def open_search_bar(self):
        try:
            search_bar = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.search_bar))
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
                EC.presence_of_element_located((By.XPATH, self.input_box))
            )
            text_input.clear()
            text_input.send_keys(product_name)
            general_logger.info("Search query entered successfully")
            time.sleep(1)
        except Exception as e:
            exception_logger.error(f"Error entering product name in search bar: {e}")
            return False
        return True

    def fetch_and_click_product(self):
        try:
            product = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.search_result))
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
                general_logger.info(f"Product Page Opened Successfully: {actual_url}||{expected_url}")
                return True
        except Exception as e:
            exception_logger.error(f"Error validating product page: {e}")
        return False

    def get_product_name(self):
        try:
            time.sleep(5)
            product_name = self.driver.find_element(By.XPATH, self.product_page).text
            general_logger.info(f"Product Name on Product Page : {product_name}")
            return product_name
        except Exception as e:
            exception_logger.error(f"Error fetching product name from product page: {e}")
            return None
        
    def add_product_to_cart(self):
        try:
            select_element = self.driver.find_element(By.XPATH, self.multiple_weight_dropdown)  
            select_exists = True 
        except NoSuchElementException:
            select_exists = False
        try:
            prices = [] 
            if select_exists:
                general_logger.info('Multiple Weights Found')
                select = Select(select_element)
                for idx in range(0, len(select.options)):
                    opt = select.options[idx]
                    WebDriverWait(self.driver, 10).until(EC.visibility_of(opt))
                    select.select_by_index(idx)
                    print(f'Non-Select: {opt.get_attribute("label")}')
                    # Extract prices
                    actualPrice = self.driver.find_element(By.XPATH, self.actualPrice_product).text
                    discountedPrice = self.driver.find_element(By.XPATH, self.discountedPrice_product).text
                    prices.append({
                        f"{opt.get_attribute('label')} actualPrice": actualPrice,
                        f"{opt.get_attribute('label')} discountedPrice": discountedPrice
                    })
                    add_to_cart = self.driver.find_element(By.XPATH, self.add_to_cart)
                    add_to_cart.click()
                    general_logger.info('Product Added to cart weight wise')
                general_logger.info(prices)
                return prices
            else:
                general_logger.info('Single Weight Found')
                variant_weight = self.driver.find_element(By.XPATH, self.single_weight_nodropdown).text
                actualPrice = self.driver.find_element(By.XPATH, self.actualPrice_product).text
                discountedPrice = self.driver.find_element(By.XPATH, self.discountedPrice_product).text
                prices.append({
                    f'{variant_weight} Actual Price': actualPrice,
                    f'{variant_weight} Discounted Price': discountedPrice
                })
                general_logger.info(prices)
                return prices
        except Exception as e:
            exception_logger.error(f"Error fetching product price from product page: {e}")
            return None

    def open_cart(self):
        pass
    
# x = SearchProduct
