from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import *
import logging
import random
import string
# Create your views here.

def login(request):
    if request.method == 'POST': #로그인 실행
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(request, username=username, password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('main:mainpage')
        else:
            return render(request, 'accounts/login.html')
        
    elif request.method == 'GET': #로그인 페이지 띄우기
        return render(request, 'accounts/login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('main:mainpage')

def signup(request):
    if request.method == "POST":
        
        if request.POST['password'] == request.POST['confirm']:
            user = User.objects.create_user(
                username = request.POST['username'],
                password=request.POST['password']
            )
            
            grade = request.POST['grade']
            department = request.POST['department']
            name = request.POST['name']
            nickname = request.POST['nickname']
            userImage = request.FILES.get('userImage')
            mytags = request.POST['mytags']
            
            #태그형식
            words = mytags.split(' ')
            tag_list = []
            for w in words:
                if len(w)>0:
                    if w[0] == '#':
                        tag_list.append(w[1:])
            
            #한줄에 편하게 POST를 받는 방식
            profile = Profile(user=user, grade=grade, department=department,name=name, nickname=nickname, userImage=userImage)
            profile.save()
            for t in tag_list:
                tag, boolean = MyTag.objects.get_or_create(mytagname=t) 
                profile.taglist.add(tag)
                
            auth.login(request, user)
            return redirect('/')
    return render(request, 'accounts/signup.html')

def emailconfirm(request, username):
    try:
        email_address = f'{username}@dgu.ac.kr'
        email_subject = '끼리 회원가입 인증메일입니다 :>'
        verification_code = generate_verification_code()
        email_message = '끼리 회원가입 인증번호\n' + verification_code

        send_mail(email_subject, email_message, '', [email_address])
        email_sent = True
    except Exception as e:
        email_sent = False

    return render(request, 'accounts/signup.html', {'email_sent': email_sent, 'verification_code': verification_code})

def generate_verification_code():
    characters = string.ascii_letters + string.digits
    verification_code = ''.join(random.choices(characters, k=6))
    return verification_code