from django.urls import path
from .views import * # main 앱 내의 views.py를 사용하기 위한 코드
from . import views

app_name = "main"
urlpatterns = [
    #path('', mainpage, name="mainpage"),
    path('mainpage/', mainpage, name="mainpage"),
    path('', firstpage, name="firstpage"),
    #path('firstpage/', firstpage, name="firstpage"),
    # path('secondpage/', secondpage, name="secondpage"),
    # path('thirdpage/', thirdpage, name="thirdpage"),
    path('new/', new, name="new"), #new 페이지 url 연결
    path('create/', create, name="create"), #create 생성페이지 url 연결
    path('<int:id>', detail, name="detail"), #id에 부합하는 detail페이지로 연결
    path('edit/<int:id>', edit, name="edit"),
    path('update/<int:id>', update, name="update"),
    path('delete/<int:id>', delete, name="delete"),
    path('search/', views.SearchView.as_view(), name='search'),
    path('maketeam1/', maketeam1, name="maketeam1"),
    path('maketeam2/', maketeam2, name="maketeam2"),
    path('teamtest1/', teamtest1, name="teamtest1"),
    path('result/<int:test_result_id>/', result, name='result'),
    path('<int:id>/volunteer', volunteer, name='volunteer'),
    path('tag/', tag_list, name="tag_list"),
    path('tag/<int:tag_id>', tag_posts, name="tag_posts"),
]