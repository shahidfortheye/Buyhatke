from selenium import webdriver
from amazoncaptcha import AmazonCaptcha
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class AmazonParser:
    def __init__(self):
        # Automatically manage ChromeDriver installation
        # service = Service(ChromeDriverManager().install())
        
        # Set up Chrome options if needed
        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--log-level=3')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        service = Service('/usr/local/bin/chromedriver')

        self.driver = webdriver.Chrome(service=service, options=options)

    def fetch_captcha_page(self):
        try:
            # Navigate to the Amazon captcha page
            self.driver.get('https://www.amazon.in/errors/validateCaptcha')
            # Get the captcha image link
            link = self.driver.find_element(By.XPATH, "//div[@class='a-row a-text-center']//img").get_attribute('src')
            captcha = AmazonCaptcha.fromlink(link)

            # Solve the captcha
            captcha_value = AmazonCaptcha.solve(captcha)
            print("Captcha Value:", captcha_value)

            # Input the captcha value in the input field
            input_field = self.driver.find_element(By.ID, "captchacharacters")
            input_field.send_keys(captcha_value)

            # Click the submit button
            button = self.driver.find_element(By.CLASS_NAME, "a-button-text")
            button.click()
        except Exception as e:
            print("An error occurred while fetching captcha:", e)

    def search_product(self,data):
        try:
            # Navigate to Amazon's search page
            html = self.driver.get('https://www.amazon.in/Plantex-Self-Adhesive-Multipurpose-Bathroom-Accessories/dp/B0B3J7Q14R/ref=sr_1_3?_encoding=UTF8&content-id=amzn1.sym.8844e7df-0ffd-4ead-86ea-172bfc8bb1a0&dib=eyJ2IjoiMSJ9.H4UbqLR06PN_0RD9nXHSRjsrIdnkcaCb6OLWHA68cnVmjf2-ivaYheRjwpzlMd-tWKIMF3iMf_Xs5NGCJ0rrxtfz6r-Z8_-qDHEVSasjqczOOPuJ5XOOY6QMQHtXJkaWcNriuXmIOg1jaOuhXXfCRuZfJM8aFSp6JGxAM3pYRnuqNhmn9uk2N8f4wLTBN30eTkxSMEqzIgLSZmkjLyzDy14gooWnAvHgvcmG4vttQ4k.QpDCENgZ5PcQ8SiM2GX3JiqBF6ewJpsURR94TyQyX3o&dib_tag=se&keywords=bathroom+hardware+and+accessories&pd_rd_r=5c00ff48-f294-4dbd-a592-437da5b584b1&pd_rd_w=oKRoi&pd_rd_wg=baCXg&pf_rd_p=8844e7df-0ffd-4ead-86ea-172bfc8bb1a0&pf_rd_r=V2FN59AEGN8A90HZX6D5&qid=1721056161&refinements=p_n_pct-off-with-tax%3A2665399031&s=home-improvement&sr=1-3')
            self.driver.implicitly_wait(10)  # Adjust wait time as necessary
            # print(self.driver.page_source)
            # Extract product title
            title = self.driver.find_element(By.ID, "productTitle").text
            price_whole = self.driver.find_element(By.CLASS_NAME, "a-price-whole").text


            ratings_element = self.driver.find_element(By.CSS_SELECTOR, "a.a-popover-trigger .a-size-base.a-color-base")
            ratings = ratings_element.text.strip()

            total_ratings_element = self.driver.find_element(By.ID, "acrCustomerReviewText")
            total_ratings = total_ratings_element.text.strip()

            image_element = self.driver.find_element(By.ID, "landingImage")
            image_url = image_element.get_attribute("src")
            # # Extract total ratings
            # total_ratings = self.driver.find_element(By.XPATH, "//span[@id='acrCustomerReviewText']").text.split()[0]

            # # Extract total reviews
            # total_reviews = self.driver.find_element(By.XPATH, "//span[@id='acrPopover']//span[@class='a-size-medium']").text.split()[0]

            # # Extract image URL
            # image_url = self.driver.find_element(By.ID, "landingImage").get_attribute("src")

            # # Set product ID and URL
            product_id = data.get("product_id")
            url = self.driver.current_url
            data = {
                    'title': title,
                    'price': price_whole,
                    'ratings': ratings,
                    'total_ratings': total_ratings,
                    'total_reviews': 0,
                    'image_url': image_url,
                    'product_id' : product_id,
                    'platform' : 'amazon',
                    'url' : url
                }
            return data
            # search_box = self.driver.find_element(By.ID, "twotabsearchtextbox")
            # # search_box.send_keys()
            # # search_box.submit()

            # # Get product details from the search results
            # self.get_product_details()
        except Exception as e:
            print("An error occurred during product search:", e)

    def get_product_details(self):
        try:
            # Example: Get the first product's title and price from the search results
            product_title = self.driver.find_element(By.XPATH, "(//span[@class='a-size-medium a-color-base a-text-normal'])[1]").text
            product_price = self.driver.find_element(By.XPATH, "(//span[@class='a-price-whole'])[1]").text
            print("Product Title:", product_title)
            print("Product Price:", product_price)
        except Exception as e:
            print("An error occurred while getting product details:", e)

    def driver_quit(self):
        # Close the browser when needed
        pass
        # self.driver.quit()

# Usage
