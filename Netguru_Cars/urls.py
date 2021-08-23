"""Netguru_Cars URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, re_path
from Cars.views import CarView, RateView, PopularView

urlpatterns = [
    path('cars/', CarView.as_view()),
    re_path(r'^cars/{\s*(?P<del_id>\d+)\s*}/?$', CarView.as_view()),
    path('rate/', RateView.as_view()),
    path('popular/', PopularView.as_view())
]
