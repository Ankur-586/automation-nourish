# import pytest

# from pages.searchProd import SearchProduct

# from settings.config import WebDriverSetup

# @pytest.fixture()
# def setup():
#     # Set up WebDriver and page objects before tests
#     driver = WebDriverSetup()
#     search_prod = SearchProduct(driver)
#     yield search_prod, driver
#     driver.quit()  # Clean up after tests

# def test_site_open(open_search_bar):
#     search_prod, driver = open_search_bar
#     search_prod.open_search_bar()
#     assert not search_page.open_search_bar():  