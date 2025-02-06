import time, cProfile

from settings.config import WebDriverSetup
from settings.log_setup import general_logger, exception_logger

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def AddProductFromSearchbar(actula_product_name: str, website_url):
    
    if not isinstance(actula_product_name, str):
        exception_logger.error("Product name should be a string")
        return
    else:
        striped_prod_name = actula_product_name.strip()
        
    # --------------------------------------------------------------------------------------------
    try:
        web_driver_setup = WebDriverSetup(headless=True)  # Change to True for headless mode
        driver = web_driver_setup.setup_driver()
        general_logger.info("WebDriver initialized successfully.")
    except Exception as e:
        exception_logger.error(f"Error initializing WebDriver: {e}")
        return
    
    # --------------------------------------------------------------------------------------------
    # Open the website
    try:
        driver.get(website_url)
        general_logger.info(f"Navigated to {website_url}")
    except Exception as e:
        exception_logger.error(f"Error loading website: {e}")
        return
    
    # --------------------------------------------------------------------------------------------
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
    
    # --------------------------------------------------------------------------------------------
    driver.implicitly_wait(10) 
    
    # --------------------------------------------------------------------------------------------
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
    
    # --------------------------------------------------------------------------------------------
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
        general_logger.info(f"Fetched product: {sorted_product_list}")
        expected_product_name = striped_prod_name.title()
        for product_name, product_url in sorted_product_list:
            if expected_product_name == product_name.title():
                driver.get(product_url)
                general_logger.info(f"Clicked on product: {product_name}, ({product_url})")
                break
    except Exception as e:
        exception_logger.error(f"Error fetching product text: {e}")
        return
    
    # --------------------------------------------------------------------------------------------
    try:
        #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h1[text()="Product Title"]')))
        product_name_on_productPage = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[1]/h1').text
        general_logger.info(f"Product name: {product_name_on_productPage}")
    except Exception as e:  
        exception_logger.error(f"Error fetching product name: {e}")
        return
    general_logger.info("Product search from search bar completed successfully.")
    
    # --------------------------------------------------------------------------------------------
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
    # Case 1: When select element exists Along with Discount. Product Example: Arhar/Toor Dal
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
    # Case 2: When select exists But Discount doesn't. Product Example: Spiral Pasta
    elif select_exists and not (discounted_exists and actual_exists):
        general_logger.info('Multiple Weights Found Without Discounted Price')
        select = Select(select_element)
        for idx in range(0, len(select.options)):
            opt = select.options[idx]
            WebDriverWait(driver, 10).until(EC.visibility_of(opt))
            select.select_by_index(idx)
            actualPrice_withOut_discount = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span').text
            prices.append({
                f"{opt.get_attribute('label')} actualPrice": actualPrice_withOut_discount
            })
            add_to_cart = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/button')
            add_to_cart.click()
        general_logger.info('Product Added to cart Without Discount')
        general_logger.info(prices)
    # Case 3: When select does not exists And Also Discount doesn't. Product Example: Moti Elaichi
    elif not select_exists and not (discounted_exists and actual_exists):
        general_logger.info('Single Weights Found Without Discounted Price')
        variant_weight = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/span').text
        actualPrice_withOut_discount = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/span/span').text
        prices.append({
            f"{variant_weight} actualPrice": actualPrice_withOut_discount
        })
        add_to_cart = driver.find_element(By.XPATH, '/html/body/main/main/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/button')
        add_to_cart.click()
        general_logger.info(f"{variant_weight} of {striped_prod_name} Added to cart")
        general_logger.info(prices)
    # Case 4: When select does not exists But Discount does. Product Example: Rai 
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
        general_logger.info('Product Added to cart With Single weight With Discount')
        general_logger.info(prices)
    else:
        # Case 5: When Add to cart button doesn't Exists Give a message and return
        exception_logger.error('Some Weird Error Happened')
        
    # --------------------------------------------------------------------------------------------
    # Cart Icon
    try:
        cart_icon_click = driver.find_element(By.XPATH, '/html/body/header/nav/div[2]/div/div/div[2]/div[2]')
        cart_icon_click.click()
        general_logger.info("Cart Icon Clicked")                    
        if website_url == 'https://nourishstore.in/':
            proceed_to_checkout_button = driver.find_element(By.XPATH, '//*[@id="headlessui-tabs-panel-:R6kt1ja:"]/div[2]/div[3]') # For Live website
        else:
            proceed_to_checkout_button = driver.find_element(By.XPATH, '//*[@id="headlessui-tabs-panel-:Rqjk6cq:"]/div[2]/div[3]') # for development website
        proceed_to_checkout_button.click()
        general_logger.info("Proceed To Checkout Button Clicked")   
    except Exception as e:
        exception_logger.error(f"Error in Cart Click Functionality: {e}")
        
    # --------------------------------------------------------------------------------------------
    try:
        # login/signup Pop-upBox
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/header/nav/div[4]/div[2]/div/div/div')) 
        )
        general_logger.info('Found The Login/SignUp Form')
        
        # Find the mobile input box and enter the mobile number
        mobile_input_box = driver.find_element(By.XPATH, '/html/body/header/nav/div[4]/div[2]/div/div/div/div/div[2]/div/div[2]/form/input')
        mobile_input_box.send_keys('8884154409')
        
        # Click the button to submit the form
        submit_button = driver.find_element(By.XPATH, '/html/body/header/nav/div[4]/div[2]/div/div/div/div/div[2]/div/div[2]/form/button')
        if submit_button.is_enabled() and submit_button.is_displayed():
            submit_button.click()
            general_logger.info("Next Button was clicked!")
        
        # Wait for the next input box to appear after submission
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/header/nav/div[4]/div[2]/div/div/div/div/div[2]/div/div[2]/form/div[2]'))
        )
        while True:
            entering_otp = input('Enter the otp: ')
            if len(entering_otp) != 6 or not entering_otp.isdigit():
                print("Invalid OTP! Please enter exactly 6 numeric digits.")
                continue
            else:
                for idx, otp_num in enumerate(entering_otp, start=1):
                    input_box =  driver.find_element(By.XPATH, f'/html/body/header/nav/div[4]/div[2]/div/div/div/div/div[2]/div/div[2]/form/div[2]/input[{idx}]')
                    input_box.send_keys(otp_num)
                    general_logger.info(f'Box Number {idx}, OTP Number: {otp_num}')
                otp_submit_button = driver.find_element(By.XPATH, '/html/body/header/nav/div[4]/div[2]/div/div/div/div/div[2]/div/div[2]/form/button')
                otp_submit_button.click()
                general_logger.info('Correct OTP! Please Procceed Further')
                invalid_message = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/header/nav/div[4]/div[2]/div/div/div/div/div[2]/div/div[2]/form/p[3]'))
                )
                # below code is not working as excpected. Enter a wrong otp and then check
                if invalid_message:
                    general_logger.info('Wrong OTP')
                    for idx in range(1, 7):  # Assuming there are 6 OTP input fields
                        input_box_clear = driver.find_element(By.XPATH, f'/html/body/header/nav/div[4]/div[2]/div/div/div/div/div[2]/div/div[2]/form/div[2]/input[{idx}]')
                        input_box_clear.clear()  # Clear the OTP input field
    except TimeoutException:
        exception_logger.error('Element Not Found')
    # --------------------------------------------------------------------------------------------
    cart_title = driver.find_element(By.XPATH, '/html/body/header/nav/div[4]/div/div[1]/div[1]/h2')
    print('cart_title',cart_title)
    
    web_driver_setup.close_driver()

if __name__ == "__main__":
    product_name = 'Nourish Nutrition Delights Combo of 3'
    website_url = 'https://nourishstore.in/'
    AddProductFromSearchbar(product_name, website_url)
    # run_var = AddProductFromSearchbar('Nourish Nutrition Delights Combo of 3')
    # cProfile.run(run_var)
    

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
'''