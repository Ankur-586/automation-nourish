import time

from settings.config import WebDriverSetup
from settings.log_setup import general_logger, exception_logger

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

def AddProductFromSearchbar(product_name: str):
    
    # if not isinstance(product_name, str):
    #         exception_logger.error("Product name should be a string")
    #         return

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
        return
    
    # Fetch product name from search results
    try:
        print('iewwwwwwwwwwwwwoeooeoeeeeeeeoooeeeeeeeeeeebjkbkjbkjbkjkjkjbeeeeeeeeeeeeeeeeeeeeessssssssssskjjkhkjhkjhkjh')
        product_list = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/header/nav/div[3]/div/div/div[2]/div/ul'))
        )
        product_list_list = []
        for i in range(0,len(product_list)):
            print(i)
            product_name = driver.find_element(By.XPATH, '/html/body/header/nav/div[3]/div/div/div[2]/div/ul/div[1]/div/div/a/p[1]').text
            product_list_list.append([product_name])
        print('product_listproduct_listproduct_list',product_list_list)
        # general_logger.info(f"Fetched product: {fetch_product_text.text}")
        print('[wirdcjurqeprjperjpepqrperpoqrpouroeuiropiroqierpr85+6et+9rf7d74g+e7h9+re7h+9weh7w+98h7w+fsfsfsfsfsf9]')
    except Exception as e:
        exception_logger.error(f"Error fetching product text: {e}")
        return
    
    # Click on the product to open the product page
    try:
        fetch_product_text.click()
        time.sleep(5)
        general_logger.info("Product page opened successfully")
        # expected_product_page_url = 'https://nourishstore.in/spices/moti-saunf'
        # actual_product_page_url = driver.current_url
        # if expected_product_page_url == actual_product_page_url:
        #     general_logger.info("Product page opened successfully")
        #     # return 'Pass'
        # exception_logger.error("Product page did not open successfully")
        # return 'Fail'
    except Exception as e:
        exception_logger.error(f"Error opening product page: {e}")
    
    try:
        product_name = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[1]/h1').text
        general_logger.info(f"Product name: {product_name}")
    except Exception as e:  
        exception_logger.error(f"Error fetching product name: {e}")
    
    # Log that everything was successful
    general_logger.info("Product search from search bar completed successfully.")
    time.sleep(5)
    
    try:
        # Try finding the select element and checking if it's present
        select_element = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/select')  
        select_exists = True  # Element found, set flag to True
    except NoSuchElementException:
        # If element is not found, set flag to False
        select_exists = False
    # Case 1: When select element exists (variants available)
    if select_exists:
        general_logger.info('Multiple Weights Found')
        select = Select(select_element)
        prices = [] 
        for idx in range(0, len(select.options)):
            opt = select.options[idx]
            WebDriverWait(driver, 10).until(EC.visibility_of(opt))
            select.select_by_index(idx)
            print(f'Non-Select: {opt.get_attribute("label")}')
            # Extract prices
            actualPrice = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span[2]').text
            discountedPrice = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span[1]').text
            prices.append({
                f"{opt.get_attribute('label')} actualPrice": actualPrice,
                f"{opt.get_attribute('label')} discountedPrice": discountedPrice
            })
            # Add to cart logic
            add_to_cart = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/button')
            add_to_cart.click()
            print('Added to cart')
        general_logger.info(prices)
    # Case 2: No select element (no variants)
    else:
        general_logger.info('Single Weights Found')
        variant_weight = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/span').text
        actualPrice = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span[2]').text
        discountedPrice = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span[1]').text
        general_logger.info(f"Variant Text: {variant_weight}, Actual Price: {actualPrice}, Discounted Price: {discountedPrice}")
    
    web_driver_setup.close_driver()

if __name__ == "__main__":
    AddProductFromSearchbar('rai')
    
'''
if suppose on the first run i have a product and the product page is different which has white box and inside that we have no select element but only span with a text 
and on the second run, supoose we have a product page which has a select then how can i perform this. 
bascialy the product page is one. ANd its structure is asllo same. but different product renders differntly. If a project has variants then a select box is rendered and if 
no variants then there is no slect box.
in this page i have a product secetion in which i am trying to selects or identity the elemtns but also in that page a crousol is being displayed which also contains '//*[@id="select1"]'
element. ANd basically why i am telling you is becasue you can understand right?

grid_class_name = driver.find_element(By.CLASS_NAME, 'grid.grid-cols-12')
ele_structure = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]') 
white_box = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div') 
general_logger.info('Inside the white Box')

if grid_class_name:
    if ele_structure:
        if white_box:
            try:
                # Try finding the select element and checking if it's present
                select_element = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/select')  
                select_exists = True  # Element found, set flag to True
            except NoSuchElementException:
                # If element is not found, set flag to False
                select_exists = False
            # Case 1: When select element exists (variants available)
            if select_exists:
                print('Select option found')
                select = Select(select_element)
                prices = [] 
                for idx in range(0, len(select.options)):
                    opt = select.options[idx]
                    WebDriverWait(driver, 10).until(EC.visibility_of(opt))
                    select.select_by_index(idx)
                    print(f'Non-Select: {opt.get_attribute("label")}')
                    # Extract prices
                    actualPrice = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span[2]').text
                    discountedPrice = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span[1]').text
                    prices.append({
                        f"{opt.get_attribute('label')} actualPrice": actualPrice,
                        f"{opt.get_attribute('label')} discountedPrice": discountedPrice
                    })
                    # Add to cart logic
                    add_to_cart = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/button')
                    add_to_cart.click()
                    print('Added to cart')
                general_logger.info(prices)
            # Case 2: No select element (no variants)
            else:
                print('No select option found')
                variant_text = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/span').text
                actualPrice = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span[2]').text
                discountedPrice = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span[1]').text
                print(f"Variant Text: {variant_text}, Actual Price: {actualPrice}, Discounted Price: {discountedPrice}")
        else:
            print('white_box not found')
    else:
        print('box not found')
else:
    print('Not grid')
'''