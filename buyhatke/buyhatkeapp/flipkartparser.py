
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import datetime
import json
import os
import requests
import random
from bs4 import BeautifulSoup as bs
import traceback
from buyhatke.config import db


class FlipkartScrapper:
    def __init__(self):
        # self.proxy = self.get_proxy()
        self.driver = self.get_driver()

    def get_proxy(self):
         url = "http://httpbin.org/ip"
         proxies = self.get_free_proxies()
         proxy_ = None
         for i in range(len(proxies)):
        
        #         #printing req number
            proxy = proxies[i]
        #         print(proxy)
            try:
                response = requests.get(url, proxies = {"http":proxy, "https":proxy})
                proxy_ = proxy
                return proxy_
            except:
                # if the proxy Ip is pre occupied
                return None
            

    def get_free_proxies(self):
        url = "https://free-proxy-list.net/"
        # request and grab content
        soup = bs(requests.get(url).content, 'html.parser')
        # to store proxies
        proxies = []
        for row in soup.find("table", attrs={"class": "table-striped"}).find_all("tr")[1:]:
            tds = row.find_all("td")
            try:
                ip = tds[0].text.strip()
                port = tds[1].text.strip()
                proxies.append(str(ip) + ":" + str(port))
            except IndexError:
                continue
        return proxies
    
    def driver_quit(self):
        self.driver.quit()
        
    def get_driver(self):
        # path = "C:/Users/Shahid.DESKTOP-JH5TIT1/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
        os.environ["DISPLAY"] = ":98"
        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--window-size=1920,1080")

        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36")
        options.add_argument("--ignore-certificate-errors")

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        # if self.proxy:
            # proxy_host = "172.17.0.1"
            # proxy_port = "8080"
            
            #     #     # Create proxy string
            # proxy = f"{proxy_host}:{proxy_port}"
        # options.add_argument(f'--proxy-server=http://{proxy}')
        driver = webdriver.Chrome(options=options)
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver
    
    def fetch_html(self, obj):
        html = None
        try:

            self.driver.get(obj.get("url"))
            # print("ppppppppppppppppppppppppppppssssssssssssssssssssssssssssssssssssss")
            html = self.driver.page_source
        except:
            print("EROOOOOOOOOOOOOOr")
        
        product_id = obj.get("product_id")
        url = obj.get("url")
        if html:
            # print(html)
            

            #  Parse HTML content using BeautifulSoup

            soup = bs(html, 'html.parser')
            element = soup.find("div", 
                                    class_="C7fEHH")
            image = soup.find("div", 
                                    class_="vU5WPQ")
            # print(element)
            # Initialize variables with None in case the elements are not found
            title = None
            price = None
            ratings = None
            total_ratings = None
            total_reviews = None
            image_url = None

            # Find the elements and assign values if found
            title_element = element.find('span', class_='VU-ZEz')
            if title_element:
                title = title_element.text.strip()

            price_element = element.find('div', class_='Nx9bqj CxhGGd')
            if price_element:
                price = price_element.text.strip()

            ratings_element = element.find('div', class_='XQDdHH')
            if ratings_element:
                ratings = ratings_element.text.strip()

            total_ratings_element = element.find('span', class_='Wphh3N')
            if total_ratings_element:
                total_ratings = total_ratings_element.text.strip()
                total_ratings = total_ratings.replace('\xa0&\xa0', ' and ')

            total_reviews_element = element.find('span', class_= 'Wphh3N')
            if total_reviews_element:
                total_reviews = total_reviews_element
            image_element = image.find('img')
            if image_element:
                image_url = image_element['src']
            try:
                data = {
                    'title': title,
                    'price': price,
                    'ratings': ratings,
                    'total_ratings': ''.join(filter(str.isdigit, total_ratings.split('and')[0])),
                    'total_reviews': ''.join(filter(str.isdigit, total_ratings.split('and')[1])),
                    'image_url': image_url,
                    'product_id' : product_id,
                    'url' : url
                }
            except Exception as E:
                data = {
                    'title': title,
                    'price': price,
                    'ratings': ratings,
                    'total_ratings': 0,
                    'total_reviews': 0,
                    'image_url': image_url
                }
        else:
            data = None
            pass

        return data


class UpdateDatatoMongo:
    def __init__(self, data):
        self.data = data

    def update_data(self):

        # URL of the API endpoint
        self.data["datetime"] = datetime.datetime.now()
        update_price(self.data)        




data = []
def pass_url(urls):

    
    obj1 = FlipkartScrapper()
    result= obj1.fetch_html(urls)

    if result:
        data.append(result)
        req = UpdateDatatoMongo(result)
        req.update_data()
        return result
    else:
        None
    obj1.driver_quit()



def update_price(obj):
    
    last_price = db.ParserUrls.find_one({"product_id": obj.get("product_id")})
    if last_price:
        if last_price.get("last_price") and obj.get("last_price") < last_price.get("last_price"):
            send_notification_to_users(obj)
        cond = {}
        cond["product_id"] = last_price["product_id"]
        update = {}
        if obj.get("reviews"):
            update["reviews"] = obj.get("reviews")
        if obj.get("ratings"):
            update["ratings"] = obj.get("ratings")
        update["lastparsed_date"] = datetime.datetime.now()
        try:
            update["average_price"] = (last_price.get("average_price")+ obj.get("last_price"))/(obj.get("parsed_days")+1)
            update["lowest_price"] = last_price.get("lowest_price") if obj.get("last_price") > last_price.get("lowest_price") else obj.get("last_price")
            update["highest_price"] = last_price.get("highest_price") if obj.get("last_price") < last_price.get("highest_price") else obj.get("last_price")
        except:
            print("error")
        update["last_price"] = obj.get("last_price")
        update["updated_time"] = obj.get("updated_time")

        db.ParserUrls.update_one(cond,{"$set":update})
    else:
        db.ParserUrls.insert_one(obj)
    add_to_price_history(obj)


def send_notification_to_users(obj):
    users = db.price_notification_users.find(
        {"product_id": obj.get("product_id"),"notification_price": {"$gte":obj.get("last_price")}})
    for i in users:
        print(i)


def add_to_price_history(obj):
    
    db.price_history.update_one(
            {"product_id":  obj.get("product_id")},
            {"$push": {"data": {"price":
                                obj.get("price"),
                                "datetime": str(datetime.date.today())}}},
                                upsert=True)
