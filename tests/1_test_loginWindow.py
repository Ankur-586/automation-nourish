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
    test_inputs = ["8884154409", "123", ""]
    for input in test_inputs:
        result = login_window.get_login_window(input)
        if input == "8884154409":  # Valid number
            assert result is True, f"Valid Mobile Number '{input}' should work, but it didn't."
        
        elif input == "123":  # Invalid number (e.g., too short or incorrect format)
            assert result is False, f"Invalid Mobile Number '{input}' should not be allowed."
        
        elif input == "":  # Empty number
            assert result is False, "Empty Mobile Number should not be allowed."

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


