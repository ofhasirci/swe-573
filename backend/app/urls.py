from django.urls import path
from app.views import homePageView, collectionManager

urlpatterns = [
    path('', homePageView, name='home'),
    path('collect', collectionManager, name='collection')
]