from django.urls import include,path
from rest_framework.routers import DefaultRouter
from . import views
urlpatterns = [
    path(r'parse-url/', views.ParseUrl.as_view()),
    path(r'add-email/', views.AddEmailNotification.as_view()),
    path(r'add-bulk-products/', views.AddProductsFromSheet.as_view()),
    path(r'update-product/', views.UpdateProduct.as_view()),
    path(r'get-all-urls/', views.GetAllUrls.as_view()),
    path(r'get-product-chart/', views.GetProductChart.as_view()),
    path(r'otp/', views.Otp.as_view()),
    path(r'get-trending-products/', views.TrendingProducts.as_view()),
    path(r'top-deals/', views.TopDeals.as_view()),
    path(r'cron/', views.Cron.as_view()),
    path(r'amazonparser/', views.amazonparser.as_view()),





    ]
