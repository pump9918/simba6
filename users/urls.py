from django.urls import path
from .views import *

app_name = "users"
urlpatterns = [
    path('mypage/<int:id>/', mypage, name="mypage"),
    path('measure/<int:id>/', measure, name="measure"),
    path('mypage/approve/<int:volunteer_id>/member/', approve_member, name="approve_member"),
    path('mypage/reject/<int:volunteer_id>/member/', reject_member, name="reject_member"),
    path('profile/<int:id>/', profile, name="profile"),
    path('measure/<int:id>/like', like, name="like"),
    path('measure/<int:id>/hate', hate, name="hate")
]