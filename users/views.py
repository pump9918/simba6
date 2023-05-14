from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User

def mypage(request):
    
    if request.method == 'GET': #로그인 페이지 띄우기
        return render(request, 'users/mypage.html')
    
    #request.user == 현재 로그인한 유저에 대한 정보를 가짐