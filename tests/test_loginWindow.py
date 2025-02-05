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
    Openlogin_window = LoginWindow(driver)
    true_status = Openlogin_window.login_window()
    assert true_status == True, "PASSED"