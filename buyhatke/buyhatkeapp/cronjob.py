# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager
from buyhatke.config import db
from buyhatkeapp.utils import update_price
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import datetime
import json

import requests
import random
from bs4 import BeautifulSoup as bs
import traceback
import os

# response = requests.get("http://65.0.104.5:8000/get-all-urls/")

# # Checking the response status code
# if response.status_code == 200:
    
#     r = response.json()
#     urls = r.get("data")
#     #print(urls)
# else:
#     urls = []
# urls = [
#     "https://www.flipkart.com/google-pixel-8a-bay-128-gb/p/itm6d2e15988f2c4?pid=MOBGYQ2MQYHU59Y2&param=4779&otracker=clp_bannerads_1_4.bannerAdCard.BANNERADS_Pixel-8a-EB-From%2BMid_mobile-phones-store_D22NK70VQT44",
#     # "https://www.flipkart.com/samsung-galaxy-s23-5g-cream-128-gb/p/itmc77ff94cdf044?pid=MOBGMFFX5XYE8MZN&lid=LSTMOBGMFFX5XYE8MZNRGKCA5&marketplace=FLIPKART&fm=productRecommendation%2Fsimilar&iid=R%3As%3Bp%3AMOBGYQ2MQYHU59Y2%3Bl%3ALSTMOBGYQ2MQYHU59Y2IR0ZZ0%3Bpt%3App%3Buid%3A01c0f369-15de-11ef-939e-73220a74c524%3B.MOBGMFFX5XYE8MZN&ppt=pp&ppn=pp&ssid=ovobe5f03q6yelts1716122435213&otracker=pp_reco_Similar%2BProducts_1_35.productCard.PMU_HORIZONTAL_SAMSUNG%2BGalaxy%2BS23%2B5G%2B%2528Cream%252C%2B128%2BGB%2529_MOBGMFFX5XYE8MZN_productRecommendation%2Fsimilar_0&otracker1=pp_reco_PINNED_productRecommendation%2Fsimilar_Similar%2BProducts_GRID_productCard_cc_1_NA_view-all&cid=MOBGMFFX5XYE8MZN",
#     # "https://www.flipkart.com/try-striped-men-round-neck-multicolor-t-shirt/p/itm13a72517f8659?pid=TSHGZZD6GVWZNUV9&lid=LSTTSHGZZD6GVWZNUV9YA0MQQ&marketplace=FLIPKART&store=clo%2Fash%2Fank%2Fedy&srno=b_1_1&otracker=hp_rich_navigation_2_1.navigationCard.RICH_NAVIGATION_Fashion~Men%2527s%2BTop%2BWear~Men%2527s%2BT-Shirts_IF56C41VGEYS&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising_NA_NAV_EXPANDABLE_navigationCard_cc_2_L2_view-all&fm=organic&iid=en_8uwtrpuAsuL9tbfADfb8vEzGqCwVsHopvp3WGYwm1AKY_Z8lJy2_jy4NTOiE3dwv5poHMj4XgqKp5f1b6VNHGg%3D%3D&ppt=hp&ppn=homepage&ssid=f4815uxrztjsosu81716122906930",
#     # "https://www.flipkart.com/aganta-remote-control-car-electronic-3d-lights-chargeable-battery-charger/p/itm2ed3ead324d52?pid=RCTGHR6AGUYDY52G&lid=LSTRCTGHR6AGUYDY52GRQPTA8&marketplace=FLIPKART&store=tng%2F56a%2Ffq8&spotlightTagId=BestsellerId_mgl%2F56m&srno=b_1_1&otracker=nmenu_sub_Baby%20%26%20Kids_0_Remote%20Control%20Toys&fm=organic&iid=d34a90d7-6d9b-41af-8bc4-39f2b444b08c.RCTGHR6AGUYDY52G.SEARCH&ppt=browse&ppn=browse&ssid=v6g4uachzpon9m9s1716122922411",
#     # "https://www.flipkart.com/rising-star-music-hub-electric-automatic-aarti-machine-gold-nut-bolts-dholak/p/itm7575ec14e41dc?pid=DHOHY552JYYGQMWD&lid=LSTDHOHY552JYYGQMWD0DOCVZ&marketplace=FLIPKART&store=ypu%2Fttd&srno=b_1_1&otracker=clp_banner_1_5.bannerX3.BANNER_musical-instruments-store_9IC1XMU47WSQ&fm=neo%2Fmerchandising&iid=en_QsMtP5W_vok_owSeQN_eRwJ6uZq_9s9eUpwOMJm31Ocw4d3Vw2qQyAXUqycw2qwIvmWxruVIGcwHds_YKpPI3Q%3D%3D&ppt=browse&ppn=browse&ssid=vt4nuduii1py72tc1716122947581",
#     # "https://www.flipkart.com/lloyd-2023-model-0-8-ton-3-star-split-inverter-ac-white/p/itmef92609770b2c?pid=ACNGPHRZX3WDQGJY&lid=LSTACNGPHRZX3WDQGJY8NHERO&marketplace=FLIPKART&store=j9e%2Fabm%2Fc54&srno=b_1_1&otracker=nmenu_sub_TVs%20%26%20Appliances_0_Split%20ACs&fm=neo%2Fmerchandising&iid=en_q-FRA56F_GPwQw4Zgj9NZoYkh5u32M5Te7BVo3P3P0AKwU1raTV9SfwYlW1IZRPtSxJ4j3nG0JAQZC1RvfbeP04IsYyWu-Pj9cxFjFAoaLk%3D&ppt=pp&ppn=pp&ssid=cn40jdhzlpklv4zk1716122967132",
#     # "https://www.flipkart.com/shoppershopee-woven-kanjivaram-silk-blend-saree/p/itm71ef461760ffe?pid=SARFBB3AHHRWGPYN&lid=LSTSARFBB3AHHRWGPYN7A34GA&marketplace=FLIPKART&store=clo%2F8on%2Fzpd%2F9og&spotlightTagId=BestsellerId_clo%2F8on%2Fzpd%2F9og&srno=b_1_6&otracker=browse&fm=neo%2Fmerchandising&iid=0cc502ac-249e-457e-b8c0-44082afe3419.SARFBB3AHHRWGPYN.SEARCH&ppt=browse&ppn=browse&ssid=jc9or26bjvkhqf401716123406743"
# ]
# urls = 
urls = db.ParserUrls.find({},{"_id":0})
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
        if self.driver:
            self.driver.quit()
        
    def get_driver(self):
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

        # Confirm binary location for google-chrome
        options.binary_location = '/usr/bin/google-chrome'

        try:
            service = Service('/usr/local/bin/chromedriver')
            driver = webdriver.Chrome(service=service, options=options)
            driver.set_page_load_timeout(120)
            driver.set_script_timeout(120)
        except Exception as e:
            print("Error starting ChromeDriver:", e)
            traceback.print_exc()
            driver = None

        return driver
    
    def fetch_html(self, obj):
        html = None
        try:
            print(str(obj.get("url")),"mmmmm")
            print(self.driver)
            self.driver.get(obj.get("url"))
            # print("ppppppppppppppppppppppppppppssssssssssssssssssssssssssssssssssssss")
            html = self.driver.page_source
            print(html)
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
        update_price(self.data)


def scrapper():
    obj1 = FlipkartScrapper()

    data = []
    for i in urls:
        result= obj1.fetch_html(i)
        print(result)
        if result:
            data.append(result)
            req = update_price(result)
            req.update_data()
    obj1.driver_quit()