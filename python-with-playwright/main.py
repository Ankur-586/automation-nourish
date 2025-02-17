from playwright.sync_api import sync_playwright

def website_search(site_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(site_url)
        print(page.title())
        page.click('#autocompleteInput')
        page.fill('#autocompleteInput', 'Rice')
        page.wait_for_timeout(1000)
        
        # locator = page.locator("//ul//div[contains(@class, 'flex justify-between items-center')]").all()
        # # locator.wait_for(state="visible")  # wait for the element to be visible
        # # x = page.getByText('//ul//div[contains(@class, "flex justify-between items-center")]')
        # for product in locator:
        #     product_name = product.(By.XPATH, self.fetched_product_name).text
        
        locator = page.locator("//ul//div[contains(@class, 'flex justify-between items-center')]")
        count = locator.count()
        product_list = set()
        for product in range(count):
            element = locator.nth(product)
            product_list.add(element.text_content())
        lst = list(product_list)
        # print(lst)
        for i in lst:
            x = i.find(")")
            print(i[0:x+1].strip())
        
        browser.close()
    
url = 'https://nourishstore.co.in/'
website_search(url)

# //*[@id="autocompleteInput"]  