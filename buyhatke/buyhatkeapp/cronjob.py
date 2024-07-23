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
from .flipkartparser import FlipkartScrapper
from .amazonparse import AmazonParser
from .utils import UpdateDatatoMongo


def scrapper():
    urls = db.ParserUrls.find({},{"_id":0})
    for obj in urls:

        result = None
        if obj.get("platform") == "flipkart":
            obj1 = FlipkartScrapper()
            result = obj1.fetch_html(obj)

        elif obj.get("platform") == "amazon":
            obj1 = AmazonParser()
            try:
                result = obj1.search_product(obj)
            except:
                obj1.fetch_captcha_page()
                result = obj1.search_product(obj)
        else:
            obj1 = FlipkartScrapper()
            result = obj1.fetch_html(obj)

            pass
        data = []

        if result:
            result["datetime"] = datetime.datetime.now()
            data.append(result)
            req = update_price(result)

        obj1.driver_quit()