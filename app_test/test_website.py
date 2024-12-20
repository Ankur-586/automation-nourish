import unittest
from unittest.mock import patch, MagicMock

from website import addProductfromSearchbar

class TestAddProductFromSearchbar(unittest.TestCase):

    @patch('src.product_operations.WebDriverSetup')  # Mock WebDriverSetup
    @patch('src.product_operations.general_logger')  # Mock logger
    @patch('src.product_operations.exception_logger')  # Mock exception logger
    def test_add_product_from_searchbar(self, mock_exception_logger, mock_general_logger, MockWebDriverSetup):
        # Create a mock driver
        mock_driver = MagicMock()
        MockWebDriverSetup.return_value.setup_driver.return_value = mock_driver

        # Call the function
        addProductfromSearchbar()

        # Check if driver.get() was called with the right URL
        mock_driver.get.assert_called_once_with("https://nourishstore.in/")
        mock_general_logger.info.assert_called_with("WebDriver initialized successfully.")
        mock_exception_logger.error.assert_not_called()  # Ensure no error occurred

if __name__ == '__main__':
    unittest.main()