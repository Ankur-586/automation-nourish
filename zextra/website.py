import time

from settings.config import WebDriverSetup
from settings.log_setup import general_logger, exception_logger

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import time

from settings.config import WebDriverSetup
from settings.log_setup import general_logger, exception_logger

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

def AddProductFromSearchbar(actula_product_name: str):
    
    if not isinstance(actula_product_name, str):
        exception_logger.error("Product name should be a string")
        return
    else:
        striped_prod_name = actula_product_name.strip()
    
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

    driver.implicitly_wait(10)    # It's good to avoid hard waits, but leaving it here temporarily for testing purposes.

    # Input the search query
    try:
        text_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="autocompleteInput"]'))
        )
        text_input.send_keys(striped_prod_name)
        general_logger.info(f"Search term {striped_prod_name} entered in the search bar.")
    except Exception as e:
        exception_logger.error(f"Error entering text in the search bar: {e}")
        return
    
    # Fetch product name from search results
    try:
        product_elements = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//ul//div[contains(@class, "flex justify-between items-center")]'))
        )
        product_data = set()
        for product_element in product_elements:
            product_name = product_element.find_element(By.XPATH, './/a/p[1]').text
            product_link = product_element.find_element(By.XPATH, './/a').get_attribute('href')
            product_data.add((product_name, product_link))
        sorted_product_list = sorted(product_data)
        expected_product_name = striped_prod_name.title()
        for product_name, product_url in sorted_product_list:
            if expected_product_name == product_name.title():
                driver.get(product_url)
                general_logger.info(f"Clicked on product: {product_name}, ({product_url})")
                break
        general_logger.info(f"Fetched product: {sorted_product_list}")
    except Exception as e:
        exception_logger.error(f"Error fetching product text: {e}")
        return
    
    try:
        #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h1[text()="Product Title"]')))
        product_name_on_productPage = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[1]/h1').text
        general_logger.info(f"Product name: {product_name_on_productPage}")
    except Exception as e:  
        exception_logger.error(f"Error fetching product name: {e}")
        return
    
    # Log that everything was successful
    general_logger.info("Product search from search bar completed successfully.")
    
    try:
        select_element = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/select')  
        select_exists = True 
    except NoSuchElementException:
        select_exists = False
    try:
        discountedPrice = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span[1]')
        discounted_exists = True
    except NoSuchElementException:
        discounted_exists = False
    try:
        actualPrice = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span[2]')
        actual_exists = True
    except NoSuchElementException:
        actual_exists = False
    prices = [] 
    # Case 1: When select element exists Along with Discount.
    if select_exists and discounted_exists and actual_exists:
        general_logger.info('Multiple Weights Found With Discounted Price')
        select = Select(select_element)
        for idx in range(0, len(select.options)):
            opt = select.options[idx]
            WebDriverWait(driver, 10).until(EC.visibility_of(opt))
            select.select_by_index(idx)
            prices.append({
                f"{opt.get_attribute('label')} actualPrice": actualPrice.text,
                f"{opt.get_attribute('label')} discountedPrice": discountedPrice.text
            })
            # Add to cart logic
            add_to_cart = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/button')
            add_to_cart.click()
            general_logger.info(f"{opt.get_attribute('label')} of {striped_prod_name} Added to cart")
        general_logger.info(prices)
    # Case 2: When select exists But Discount doesn't.
    elif select_exists and not (discounted_exists and actual_exists):
        general_logger.info('Multiple Weights Found Without Discounted Price')
        select = Select(select_element)
        for idx in range(0, len(select.options)):
            opt = select.options[idx]
            WebDriverWait(driver, 10).until(EC.visibility_of(opt))
            select.select_by_index(idx)
            actualPrice_withOut_discount = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span').text
            prices.append({
                f"{opt.get_attribute('label')} actualPrice": actualPrice_withOut_discount,
            })
            add_to_cart = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/button')
            add_to_cart.click()
        general_logger.info('Product Added to cart Without Discount')
        general_logger.info(prices)
    # Case 3: When select does not exists And Also Discount doesn't.
    elif not select_exists and not (discounted_exists and actual_exists):
        general_logger.info('Single Weights Found Without Discounted Price')
        print('Condition number 3')
    # Case 4: When select does not exists But Discount does.
    elif not select_exists and discounted_exists and actual_exists:
        general_logger.info('Single Weights Found With Discounted Price')
        variant_weight = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/span').text
        # actualPrice = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span[2]').text
        # discountedPrice = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span[1]').text
        prices.append({
            f'{variant_weight} Actual Price': actualPrice.text,
            f'{variant_weight} Discounted Price': discountedPrice.text
        })
        add_to_cart = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/button')
        add_to_cart.click()
        general_logger.info('Product Added to cart With Single weight')
        general_logger.info(prices)
    else:
        # Case 5: When Add to cart button doesn't Exists Give a message and return
        exception_logger.error('Some Weird Error Happened')

    try:
        cart_icon_click = driver.find_element(By.XPATH, '/html/body/header/nav/div[2]/div/div/div[2]/div[2]')
        cart_icon_click.click()                    
        proceed_to_checkout_button = driver.find_element(By.XPATH, '//*[@id="headlessui-tabs-panel-:R6kt1ja:"]/div[2]/div[3]')
        proceed_to_checkout_button.click()

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/header/nav/div[4]/div[2]/div/div/div'))
            )
            print('Found The Login/SignUp Form')
            # Find the mobile input box and enter the mobile number
            mobile_input_box = driver.find_element(By.XPATH, '/html/body/header/nav/div[4]/div[2]/div/div/div/div/div[2]/div/div[2]/form/input')
            mobile_input_box.send_keys('8884154409')
            # Click the button to submit the form
            submit_button = driver.find_element(By.XPATH, '/html/body/header/nav/div[4]/div[2]/div/div/div/div/div[2]/div/div[2]/form/button')
            submit_button.click()
            # Wait for the next input box to appear after submission
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/header/nav/div[4]/div[2]/div/div/div/div/div[2]/div/div[2]/form/div[2]'))
            )
            print('6 input box found')
            entering_otp = input('Enter the otp: ')
            
            
        except TimeoutException:
            print('Not Found')
            
    except Exception as e:
        exception_logger.error(f"Error in Cart Click Functionality: {e}")
    
    web_driver_setup.close_driver()

if __name__ == "__main__":
    # striped_prod_name = input('Enter Product Name: ').strip()
    AddProductFromSearchbar('Nourish Nutrition Delights Combo of 3')
    
'''
fetch a perticular element from list and fetch it from list
https://www.w3schools.com/python/trypython.asp?filename=demo_default
get position of an element present inside a python list
prod_list = ['Rai','Ghee','Atta']
prod_name = 'rai'
if prod_name.title() in prod_list:
   print(True)
# ------------------------------------------------------------------------------------
'''
# def AddProductFromSearchbar(actula_product_name: str):
    
#     # if not isinstance(product_name, str):
#     #         exception_logger.error("Product name should be a string")
#     #         return

#     try:
#         web_driver_setup = WebDriverSetup(headless=True)  # Change to True for headless mode
#         driver = web_driver_setup.setup_driver()
#         general_logger.info("WebDriver initialized successfully.")
#     except Exception as e:
#         exception_logger.error(f"Error initializing WebDriver: {e}")
#         return

#     # Open the website
#     try:
#         driver.get("https://nourishstore.in/")
#         general_logger.info("Navigated to nourishstore.in.")
#     except Exception as e:
#         exception_logger.error(f"Error loading website: {e}")
#         return

#     # Click on the search bar
#     try:
#         search_bar_click = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, '/html/body/header/nav/div[3]'))
#         )
#         search_bar_click.click()
#         general_logger.info("Search bar clicked.")
#     except Exception as e:
#         exception_logger.error(f"Search Bar Exception: {e}")
#         return

#     time.sleep(5)  # It's good to avoid hard waits, but leaving it here temporarily for testing purposes.

#     # Input the search query
#     try:
#         text_input = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, '//*[@id="autocompleteInput"]'))
#         )
#         text_input.send_keys(actula_product_name)
#         general_logger.info(f"Search term {actula_product_name} entered in the search bar.")
#     except Exception as e:
#         exception_logger.error(f"Error entering text in the search bar: {e}")
#         return
    
#     # Fetch product name from search results
#     try:
#         product_list = WebDriverWait(driver, 10).until(
#             EC.visibility_of_all_elements_located((By.XPATH, '//ul//div[contains(@class, "flex justify-between items-center")]'))
#         )
#         # List to hold product names
#         all_product_list = set()
#         # Loop through each product element
#         for product in product_list:
#             #print(f"Processing product {index + 1}")  # Prints the index of the current product
#             product_name = product.find_element(By.XPATH, './/a/p[1]').text
#             product_link = product.find_element(By.XPATH, './/a').get_attribute('href')
#             all_product_list.add((product_name,product_link))
#         products_list = list(all_product_list)
#         products_list.sort()
#         print('jrfkdajflk',products_list)
#         expected_prod = actula_product_name.title()
#         for prod in products_list:
#             products, product_url = prod
#             if expected_prod == products:
#                 product_url.click()
#         general_logger.info(f"Fetched product: {products_list}")
#     except Exception as e:
#         exception_logger.error(f"Error fetching product text: {e}")
#         return
    
#     try:
#         #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h1[text()="Product Title"]')))
#         product_name = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[1]/h1').text
#         general_logger.info(f"Product name: {product_name}")
#     except Exception as e:  
#         exception_logger.error(f"Error fetching product name: {e}")
    
#     # Log that everything was successful
#     general_logger.info("Product search from search bar completed successfully.")
#     time.sleep(5)
    
#     try:
#         # Try finding the select element and checking if it's present
#         select_element = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/select')  
#         select_exists = True  # Element found, set flag to True
#     except NoSuchElementException:
#         # If element is not found, set flag to False
#         select_exists = False
#     # Case 1: When select element exists (variants available)
#     if select_exists:
#         general_logger.info('Multiple Weights Found')
#         select = Select(select_element)
#         prices = [] 
#         for idx in range(0, len(select.options)):
#             opt = select.options[idx]
#             WebDriverWait(driver, 10).until(EC.visibility_of(opt))
#             select.select_by_index(idx)
#             print(f'Non-Select: {opt.get_attribute("label")}')
#             # Extract prices
#             actualPrice = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span[2]').text
#             discountedPrice = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span[1]').text
#             prices.append({
#                 f"{opt.get_attribute('label')} actualPrice": actualPrice,
#                 f"{opt.get_attribute('label')} discountedPrice": discountedPrice
#             })
#             # Add to cart logic
#             add_to_cart = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/button')
#             add_to_cart.click()
#             print('Added to cart')
#         general_logger.info(prices)
#     # Case 2: No select element (no variants)
#     else:
#         general_logger.info('Single Weights Found')
#         variant_weight = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/span').text
#         actualPrice = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span[2]').text
#         discountedPrice = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span[1]').text
#         general_logger.info(f"Variant Text: {variant_weight}, Actual Price: {actualPrice}, Discounted Price: {discountedPrice}")
    
#     web_driver_setup.close_driver()

# if __name__ == "__main__":
#     AddProductFromSearchbar('Moti')
'''
fetch a perticular element from list and fetch it from list
https://www.w3schools.com/python/trypython.asp?filename=demo_default
get position of an element present inside a python list
prod_list = ['Rai','Ghee','Atta']
prod_name = 'rai'
if prod_name.title() in prod_list:
   print(True)

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