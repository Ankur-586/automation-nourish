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
        
        locator = page.locator("//ul//div[contains(@class, 'flex justify-between items-center')]").all()
        # locator.wait_for(state="visible")  # wait for the element to be visible
        # x = page.getByText('//ul//div[contains(@class, "flex justify-between items-center")]')
        for link in locator:
            text = link.text_content()
            href = link.get_attribute('href')

            print("Link text is", text)
            print("Link URL is", href)
        
        # locator = page.locator("//ul//div[contains(@class, 'flex justify-between items-center')]")
        # count = locator.count()
        # product_data = set()
        # for product in range(count):
        #     element = locator.nth(product)
        #     product_data.add(element.text_content())
        # sorted_product_list = sorted(product_data)
        # product_list = [item for item in sorted_product_list]
        # for each_product in product_list:
        #     products = each_product[0:each_product.find(")")+1].strip()
        #     print(products)
            
        browser.close()
    
url = 'https://nourishstore.co.in/'
website_search(url)

# //*[@id="autocompleteInput"]  