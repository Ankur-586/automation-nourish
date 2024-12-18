from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from settings.log_setup import exception_logger, general_logger

from fake_useragent import UserAgent


class WebDriverSetup:
    
    def __init__(self, headless=True, ignore_cert_errors=True, user_agent=None):
        self.headless = headless
        self.ignore_cert_errors = ignore_cert_errors
        self.user_agent = user_agent or self.get_random_user_agent()
        self.driver = None
        
    def get_random_user_agent(self):
        try:
            ua = UserAgent()
            return ua.random
        except Exception as e:
            exception_logger.error(f"Error generating User-Agent: {e}")
    
    def setup_driver(self):
        chrome_options = Options()
        
        # User-Agent
        chrome_options.add_argument(f'--user-agent={self.user_agent}')
        
        # Headless mode
        if self.headless:
            chrome_options.add_argument("--headless=new")
        
        # Ignore certificate errors
        if self.ignore_cert_errors:
            chrome_options.add_argument("ignore-certificate-errors")
        
        # Set window size
        chrome_options.add_argument("start-maximized")
        
        # Setup path for ChromeDriver dynamically from an environment variable (optional)
        # chrome_driver_path = os.getenv('CHROME_DRIVER_PATH', '/path/to/chromedriver')  # Update the default path
        # if not os.path.exists(chrome_driver_path):
        #     logger.error(f"ChromeDriver not found at {chrome_driver_path}")
        #     raise FileNotFoundError(f"ChromeDriver not found at {chrome_driver_path}")
        
        # Initialize WebDriver
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            general_logger.info(f"WebDriver setup complete with User-Agent: {self.user_agent}")
        except Exception as e:
            exception_logger.error(f"Failed to set up WebDriver: {e}")
            raise
        
        return self.driver
    
    def close_driver(self):
        if self.driver:
            self.driver.quit()
            general_logger.info("WebDriver closed successfully.")
        else:
            exception_logger.warning("WebDriver was not initialized.")

# def setup():
    
#     # Random Useragent to hit the url
#     ua = UserAgent()
#     user_agent = ua.random
#     print(f'User Agent for the current request: {user_agent}')

#     chrome_options = Options()
#     chrome_options.add_argument(f'--user-agent={user_agent}')
#     chrome_options.add_argument("--headless=new")
#     chrome_options.add_argument("ignore-certificate-errors")

#     driver = webdriver.Chrome(options=chrome_options)
#     driver.maximize_window() # this is used to maximize the window size
#     return driver  can i improve this? I have this code in a config.py file which is inside a settings folder i made. and the other py files which will use this are in the main folder 