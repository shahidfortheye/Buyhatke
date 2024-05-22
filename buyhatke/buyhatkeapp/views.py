from rest_framework.views import APIView
from rest_framework import permissions
import requests
import pandas as pd
from io import StringIO

import json
from .utils import update_price

import buyhatkeapp.utils as ui_utils
from datetime import datetime
from buyhatke.config import db
# Create your views here.


class PublicEndpoint(permissions.BasePermission):
    def has_permission(self, request, view):
        return True


class ParseUrl(APIView):

    def get(self, request):
        # data = ParserUrls.objects.filter()
        product_id = request.query_params.get("product_id")
        data = db.ParserUrls.find_one({"product_id": product_id})
        del data["_id"]
        return ui_utils.handle_response({}, data=data, success=True)

    def post(self, request):
        class_name = self.__class__.__name__
        data = request.data
        if data:
            db.ParserUrls.insert_one({
                "url": data.get("url"),
                "product_id": data.get("product_id"),
                "product_name":  data.get("product_name"),
                "reviews":  data.get("reviews"),
                "ratings":  data.get("ratings"),
                "parsed_days":  0,
                "lowest_price": data.get("lowest_price"),
                "highest_price": data.get("highest_price"),
                "average_price": data.get("highest_price"),
                "created_time": datetime.now(),
                "updated_time": datetime.now(),
                "lastparsed_date": datetime.now(),
                "last_price": "",
                "platform": data.get("platform")})
        return ui_utils.handle_response(class_name, data=data, success=True)


class AddEmailNotification(APIView):
    def get(self, request):
        # data = ParserUrls.objects.filter()
        data = db.price_notification_users.find({
            "email_id": request.query_params.get("email_id")})
        data_ = []
        for i in data:

            del i["_id"]
            data_.append(i)
        return ui_utils.handle_response({}, data=data_, success=True)

    def post(self, request):
        data = request.data
        if data:
            db.price_notification_users.update_one(
                {
                    "product_id": data.get("product_id"),
                    "email_id": data.get("email_id")},
                {"$set": {
                    "created_time": datetime.now(),
                    "updated_time": datetime.now(),
                    "last_notification_date": "",
                    "notification_price":  data.get("notification_price"),
                    "status": "Active"
                }
                }, upsert=True)
            return ui_utils.handle_response({}, data=data, success=True)

    def put(self, request):
        class_name = self.__class__.__name__
        data = request.data
        if data:
            update = {}
            if data["notification_price"]:
                update["notification_price"] = data["notification_price"]
            if data["status"]:
                update["status"] = data["status"]
            db.price_notification_users.update_one(
                {
                    "product_id": data.get("product_id"),
                    "email_id": data.get("email_id")},
                {"$set": update}, upsert=False)

        return ui_utils.handle_response(class_name, data="updated sucessfully", success=True)


class AddProductsFromSheet(APIView):

    def post(self, request):
        class_name = self.__class__.__name__
        url = """https://docs.google.com/spreadsheets/d/e/2PACX-1vTx1Rd41dQKT\
                OqdGsaPGAtRXryVhADpbFzDMcQfb6ZYYqm8YCVKlL9reIlflUzguVjjtn_MNmFy5UlB\
                /pub?gid=0&single=true&output=csv"""
        response = requests.get(url)
        if response.status_code == 200:
            # Decode the content as text
            csv_data = response.content.decode('utf-8')
            # Parse the CSV data into a DataFrame
            df = pd.read_csv(StringIO(csv_data))
            # Now 'df' contains your data from the Google Sheets CSV file
            print(df.head())
            json_data = df.to_json(orient='records')
            json_data = json.loads(json_data)

            for i in json_data:
                if i.get("Product Id") and i.get("Url"):
                    print("yes")
                    i["datetime"] = datetime.now()
                    update_price(i)
                else:
                    print("lknsdjchsj")
        return ui_utils.handle_response(class_name,
                                        data=json_data, success=True)
