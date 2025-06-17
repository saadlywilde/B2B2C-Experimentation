"""
URL configuration for b2b2c project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from quotes import views as quote_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", quote_views.new_quote, name="new_quote"),
    path("load-products/", quote_views.load_products, name="load_products"),
    path("load-options/", quote_views.load_options, name="load_options"),
    path("quote-price/", quote_views.quote_price, name="quote_price"),
    path("quote/<int:quote_id>/", quote_views.quote_detail, name="quote_detail"),
]
