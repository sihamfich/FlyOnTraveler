from django.urls import path
from .views import home

app_name = 'Settings'

urlpatterns = [

    path('', home, name='home'),
]