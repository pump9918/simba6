from django.urls import path
from .views import *

app_name = "users"
urlpatterns = [
    path('mypage/<int:id>/', mypage, name="mypage"),
    path('measure/', measure, name="measure"),
    path('profile/', profile, name="profile"),
    path('mypage/approve/<int:volunteer_id>/member/', approve_member, name="approve_member"),
    path('mypage/reject/<int:volunteer_id>/member/', reject_member, name="reject_member"),
]