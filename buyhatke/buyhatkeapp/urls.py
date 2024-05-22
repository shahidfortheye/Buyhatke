from django.urls import include,path
from rest_framework.routers import DefaultRouter
from . import views
urlpatterns = [
    path(r'parse-url/', views.ParseUrl.as_view()),
    path(r'add-email/', views.AddEmailNotification.as_view()),
    path(r'add-bulk-products/', views.AddProductsFromSheet.as_view()),
    ]