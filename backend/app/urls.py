from django.urls import path
from . import views

urlpatterns = [
    path('search', views.search, name='search'),
    path('hello', views.homePageView, name='hello')
]