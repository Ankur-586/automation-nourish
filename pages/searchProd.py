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
        self.product_elements_search_bar = '//ul//div[contains(@class, "flex justify-between items-center")]'
        self.fetched_product_name = './/a/p[1]'
        self.fetched_product_url = './/a'
        self.product_page = '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[1]/h1'
        self.multiple_weight_dropdown = '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/select'
        self.single_weight_nodropdown = '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/span'
        self.no_discountedPrice = '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span'
        self.actualPrice_product = '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span[2]'
        self.discountedPrice_product = '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span[1]'
        self.add_to_cart = '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/button'
        # self.open_cart_with_product = ''

    def wait_for_element(self, by, locator, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, locator))
            )
        except Exception as e:
            exception_logger.error(f"Element {locator} not found: {e}")
            return None
    
    def open_search_bar(self):
        try:
            search_bar = self.wait_for_element(By.XPATH, self.search_bar)
            search_bar.click()
            general_logger.info("SearchBar clicked successfully")
            return True
        except Exception as e:
            exception_logger.error(f"Error opening search bar: {e}")
            return False
    
    def enter_search_query(self, striped_prod_name):
        try:
            text_input = self.wait_for_element(By.XPATH, self.input_box)
            text_input.clear()
            text_input.send_keys(striped_prod_name)
            general_logger.info("Search query entered successfully")
            return True
        except Exception as e:
            exception_logger.error(f"Error entering product name in search bar: {e}")
            return False

    def fetch_and_click_product(self, striped_prod_name):
        try:
            product_elements = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, self.product_elements_search_bar))
            )
            product_data = set()
            for product_element in product_elements:
                product_name = product_element.find_element(By.XPATH, self.fetched_product_name).text
                product_link = product_element.find_element(By.XPATH, self.fetched_product_url).get_attribute('href')
                product_data.add((product_name, product_link))
            sorted_product_list = sorted(product_data)
            general_logger.info(sorted_product_list)
            expected_product_name = striped_prod_name.title()
            for product_name, product_url in sorted_product_list:
                if expected_product_name == product_name.title():
                    self.driver.get(product_url)
                    general_logger.info(f"Clicked on product: {product_name}, ({product_url})")
                    break
            return product_name
        except Exception as e:
            exception_logger.error(f"Error fetching or clicking on product: {e}")
            return None

    def get_product_name(self):
        try:
            time.sleep(5)
            product_name = self.driver.find_element(By.XPATH, self.product_page).text
            general_logger.info(f"Product Name on Product Page : {product_name}")
            return product_name
        except Exception as e:
            exception_logger.error(f"Error fetching product name from product page: {e}")
            return None
        
    def add_product_to_cart(self, striped_prod_name):
        
        try:
            select_element = self.driver.find_element(By.XPATH, self.multiple_weight_dropdown)  
            select_exists = True 
        except NoSuchElementException:
            select_exists = False
            
        try:
            actualPrice = self.driver.find_element(By.XPATH, self.actualPrice_product)
            actual_exists = True
        except NoSuchElementException:
            actual_exists = False
            
        try:
            discountedPrice = self.driver.find_element(By.XPATH, self.discountedPrice_product)
            discounted_exists = True
        except NoSuchElementException:
            discounted_exists = False
        
        # add_to_cart_button = self.driver.find_element(By.XPATH, self.add_to_cart)
        prices = [] 
        
        # Case 1: When select element exists Along with Discount. Product Example: Arhar/Toor Dal
        if select_exists:
            general_logger.info('Multiple Weights Found With Discounted Price')
            select = Select(select_element)
            for idx in range(0, len(select.options)):
                opt = select.options[idx]
                WebDriverWait(self.driver, 10).until(EC.visibility_of(opt))
                select.select_by_index(idx)
                prices.append({
                    f"{opt.get_attribute('label')} actualPrice": actualPrice.text,
                    f"{opt.get_attribute('label')} discountedPrice": discountedPrice.text
                })
                add_to_cart = self.driver.find_element(By.XPATH, self.add_to_cart)
                add_to_cart.click()
                general_logger.info(f"{opt.get_attribute('label')} of {striped_prod_name} Added to cart")
            general_logger.info(prices)
            return prices
        
        # Case 2: When select exists But Discount doesn't. Product Example: Spiral Pasta
        elif select_exists and not (discounted_exists and actual_exists):
            general_logger.info('Multiple Weights Found Without Discounted Price')
            select = Select(select_element)
            for idx in range(0, len(select.options)):
                opt = select.options[idx]
                WebDriverWait(self.driver, 10).until(EC.visibility_of(opt))
                select.select_by_index(idx)
                actualPrice_withOut_discount = self.driver.find_element(By.XPATH, self.no_discountedPrice).text
                prices.append({
                    f"{opt.get_attribute('label')} actualPrice": actualPrice_withOut_discount
                })
                add_to_cart = self.driver.find_element(By.XPATH, self.add_to_cart)
                add_to_cart.click()
            general_logger.info(f"{opt.get_attribute('label')} of {striped_prod_name} Added to cart")
            return prices
            
        # Case 3: When select does not exists And Also Discount doesn't. Product Example: Moti Elaichi
        elif not select_exists and not (discounted_exists and actual_exists):
            general_logger.info('Single Weights Found Without Discounted Price')
            variant_weight = self.driver.find_element(By.XPATH, self.single_weight_nodropdown).text
            actualPrice_withOut_discount = self.driver.find_element(By.XPATH, self.no_discountedPrice).text
            prices.append({
                f"{variant_weight} actualPrice": actualPrice_withOut_discount
            })
            add_to_cart = self.driver.find_element(By.XPATH, self.add_to_cart)
            add_to_cart.click()
            general_logger.info(f"{variant_weight} of {striped_prod_name} Added to cart")
            return prices
        
        # Case 4: When select does not exists But Discount does. Product Example: Rai 
        elif not select_exists and discounted_exists and actual_exists:
            general_logger.info('Single Weights Found With Discounted Price')
            variant_weight = self.driver.find_element(By.XPATH, self.single_weight_nodropdown).text
            prices.append({
                f'{variant_weight} Actual Price': actualPrice.text,
                f'{variant_weight} Discounted Price': discountedPrice.text
            })
            add_to_cart = self.driver.find_element(By.XPATH, self.add_to_cart)
            add_to_cart.click()
            general_logger.info(f"{variant_weight} of {striped_prod_name} Added to cart")
            return prices
        
        # # Case 5: When Add to cart button doesn't Exist Means Product is out of stock and can't be added to cart
        # elif not select_exists and not (discounted_exists and actual_exists) and not add_to_cart_button:
        #     general_logger.info(f"{striped_prod_name} is Out of Stock")
        
        else:
            exception_logger.error('Some Weird Error happend')

    def open_cart(self):
        pass
    
# x = SearchProduct
'''
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
'''