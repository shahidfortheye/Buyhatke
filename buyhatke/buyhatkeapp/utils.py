from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from buyhatke.config import db
from datetime import datetime



def handle_response(object_name, data=None, headers=None, content_type=None, exception_object=None, success=False, request=None):
    """
    Args:
        success: determines whether to send success or failure messages
        object_name: The function or class where the error occurs
        data: The user error which you want to display to user's on screens
        exception_object: The exception object caught. an instance of Exception, KeyError etc.
        headers: the dict of headers
        content_type: The content_type.
        request: The request param

        This method can later be used to log the errors.

    Returns: Response object

    """
    if not success:
        # prepare the object to be sent in error response
        data = {
            'general_error': data,
            'system_error': get_system_error(exception_object),
            'culprit_module': object_name,
        }
        if request:
            # fill the data with more information about request
            data['request_data'] = request.data
            data['request_url'] = request.build_absolute_uri()
            data['request_method'] = request.META.get('REQUEST_METHOD')
            data['django_settings_module'] = request.META.get('DJANGO_SETTINGS_MODULE')
            data['http_origin'] = request.META.get('HTTP_ORIGIN')
            data['virtual_env'] = request.META.get('VIRTUAL_ENV')
            data['server_port'] = request.META.get('SERVER_PORT')
            data['user'] = request.user.username if request.user else None

        if isinstance(exception_object, PermissionDenied):
            return Response({'status': False, 'data': data}, headers=headers, content_type=content_type, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'status': False, 'data': data}, headers=headers, content_type=content_type, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'status': True, 'data': data}, headers=headers, content_type=content_type,  status=status.HTTP_200_OK)


def get_system_error(exception_object):
    """
    Takes an exception object and returns system error.
    Args:
        exception_object:

    Returns: system error

    """
    if not exception_object:
        return []
    return str(exception_object.args) if exception_object.args else str(
        exception_object) if exception_object else ""

def update_price(obj):
    last_price = db.ParserUrls.find_one({"product_id": obj.get("product_id")})
    if last_price:
        if last_price.get("last_price") and  obj.get("last_price") < last_price.get("last_price"):
            send_notification_to_users(obj)
            print("yyyyyyyyyyy")
        cond = {}
        cond["product_id"] = last_price["product_id"]
        update = {}
        if obj.get("reviews"):
            update["reviews"] = obj.get("reviews")
        if obj.get("ratings"):
            update["ratings"] = obj.get("ratings")
        update["lastparsed_date"] = datetime.now()
        update["average_price"] = (last_price.get("average_price")+ obj.get("last_price"))/(obj.get("parsed_days")+1)
        update["lowest_price"] = last_price.get("lowest_price") if obj.get("last_price") > last_price.get("lowest_price") else obj.get("last_price")
        update["highest_price"] = last_price.get("highest_price") if obj.get("last_price") < last_price.get("highest_price") else obj.get("last_price")
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
                                "datetime": obj.get("datetime")}}},
                                upsert=True)