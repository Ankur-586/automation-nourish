from playwright.sync_api import sync_playwright

def website_search(site_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(site_url)
        print(page.title())
        page.click('#autocompleteInput')
        page.fill('#autocompleteInput', 'Dal')
        browser.close()
    
url = 'https://nourishstore.co.in/'
website_search(url)

# //*[@id="autocompleteInput"]  