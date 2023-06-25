from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from main.models import *
from django.db.models import Prefetch

def mypage(request, id):
    user = get_object_or_404(User, pk=id)
    result = TestResult.objects.first()
    posts = Post.objects.filter(writer=user)
    volunteers = []
    for post in posts:
        post_volunteers = Volunteer.objects.filter(post=post)
        volunteers.append({
            'post': post,
            'volunteers': post_volunteers
        })
    context = {
        'user': user,
        'volunteers': volunteers,
        'result': result,
    }
    return render(request, "users/mypage.html", context)
    
def measure(request):
    return render(request, 'users/measure.html')

def profile(request):
    return render(request, 'users/profile.html')