from settings.config import WebDriverSetup
from settings.log_setup import general_logger, exception_logger

from pages.login_window import LoginWindow

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
    
def test_open_webSite(driver_setup):
    driver = driver_setup
    try:
        driver.get("https://nourishstore.in/")
        general_logger.info("Navigated to nourishstore.in")
    except Exception as e:
        exception_logger.error(f"Error loading website: {e}")
        pytest.fail(f"Failed to load website: {e}")
        driver.close()
        
def test_openloginWindow(driver_setup):
    driver = driver_setup
    driver.get("https://nourishstore.in/")
    openLogin_window = LoginWindow(driver)
    
    assert openLogin_window.open_login_window(), "Login window did not open as expected"

def test_valid_mobile_number(driver_setup):
    """
    Test case for valid mobile number input in the login form.
    """
    driver = driver_setup
    driver.get("https://nourishstore.in/")
    login_window = LoginWindow(driver)
    
    mobile_number = "8884154409"  # Replace with a valid mobile number for your test
    result = login_window.get_login_window(mobile_number)
    
    assert result is True, "Login pop-up did not function correctly with valid mobile number."


# def test_invalid_mobile_number(driver_setup):
#     """
#     Test case for invalid mobile number input in the login form.
#     """
#     driver = driver_setup
#     driver.get("https://nourishstore.in/")
#     login_window = LoginWindow(driver)
    
#     invalid_mobile_number = "123"  # A short or invalid mobile number
#     result = login_window.get_login_window(invalid_mobile_number)
    
#     assert result is False, "Login pop-up allowed invalid mobile number."


# def test_empty_mobile_number(driver_setup):
#     """
#     Test case for empty mobile number input.
#     """
#     driver = driver_setup
#     driver.get("https://nourishstore.in/")
#     login_window = LoginWindow(driver)
    
#     empty_mobile_number = ""  # Empty input for mobile number
#     result = login_window.get_login_window(empty_mobile_number)
    
#     assert result is False, "Login pop-up allowed empty mobile number."


# def test_submit_button_disabled(driver_setup):
#     """
#     Test case where the submit button is disabled (e.g., after entering an invalid mobile number).
#     """
#     driver = driver_setup
#     driver.get("https://nourishstore.in/")
#     login_window = LoginWindow(driver)
    
#     mobile_number = "123456"  # An invalid number that would result in a disabled button (example scenario)
#     result = login_window.get_login_window(mobile_number)
    
#     assert result is False, "Submit button should be disabled but was clickable."


# def test_login_pop_up_not_found(driver_setup):
#     """
#     Test case where the login pop-up does not appear.
#     """
#     driver = driver_setup
#     driver.get("https://nourishstore.in/")
#     login_window = LoginWindow(driver)
    
#     mobile_number = "9876543210"  # Any mobile number
#     result = login_window.get_login_window(mobile_number)
    
#     assert result is False, "Login pop-up window was not found."