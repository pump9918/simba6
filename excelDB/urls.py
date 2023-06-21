from django.urls import path
from .views import *

app_name = "excelDB"
urlpatterns = [
    path('', excel, name="excel"),
]