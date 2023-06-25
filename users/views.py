from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from main.models import *

def mypage(request, id):
    user = get_object_or_404(User, pk=id)
    result = TestResult.objects.first()
    context = {
        'user' : user,
        'posts' : Post.objects.filter(writer=user),
        'result': result,
    }
    return render(request, "users/mypage.html", context)
    
def measure(request):
    return render(request, 'users/measure.html')

def profile(request):
    return render(request, 'users/profile.html')