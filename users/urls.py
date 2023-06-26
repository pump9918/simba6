from django.urls import path
from .views import *

app_name = "users"
urlpatterns = [
    path('mypage/<int:id>/', mypage, name="mypage"),
    path('measure/', measure, name="measure"),
    path('profile/<int:id>/', profile, name="profile"),
]