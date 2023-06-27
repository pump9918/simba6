from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from main.models import *
from django.db.models import Prefetch

def mypage(request, id):
    user = get_object_or_404(User, pk=id)
    profile = user.profile
    result = TestResult.objects.first()
    posts = Post.objects.filter(writer=user)
    mytaglist = profile.taglist.all()
    volunteers = []
    for post in posts:
        post_volunteers = Volunteer.objects.filter(post=post)
        volunteers.append({
            'post': post,
            'volunteers': post_volunteers
        })
    apply = Volunteer.objects.filter(user=user)
    context = {
        'user': user,
        'volunteers': volunteers,
        'result': result,
        'apply' : apply,
        'mytaglist' : mytaglist,
    }
    return render(request, "users/mypage.html", context)
    
def measure(request, id):
    user = get_object_or_404(User, pk=id)
    projects = Volunteer.objects.filter(user=user, info='accepted')
    my_projects = []
    for project in projects:
        member = Volunteer.objects.filter(post=project.post)
        my_projects.append({
            'project': project,
            'member': member
        })
    
    my_posts = Post.objects.filter(writer=user)
    my_post_projects = []
    for my_post in my_posts:
        my_post_member = Volunteer.objects.filter(post=my_post, info='accepted')
        my_post_projects.append({
            'project': my_post,
            'member': my_post_member
        })

    context = {
        'my_projects': my_projects,
        'user': user,
        'my_post_projects': my_post_projects,
    }
    return render(request, 'users/measure.html', context)

def approve_member(request, volunteer_id):
    volunteer = Volunteer.objects.get(id=volunteer_id)
    volunteer.info = 'accepted'
    volunteer.save()

    return redirect('users:mypage', id=volunteer.post.writer.profile.id)

def reject_member(request, volunteer_id):
    volunteer = Volunteer.objects.get(id=volunteer_id)
    volunteer.info = 'rejected'
    volunteer.save()

    return redirect('users:mypage', id=volunteer.post.writer.profile.id)

def profile(request, id):
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
    apply = Volunteer.objects.filter(user=user)
    context = {
        'user': user,
        'volunteers': volunteers,
        'result': result,
        'apply' : apply
    }
    return render(request, 'users/profile.html', context)

def like(request, id):
    user = request.user
    liked_user = get_object_or_404(User, pk=id)
    is_liker = user.profile in liked_user.profile.likers.all()
    if is_liker:
        user.profile.likes.remove(liked_user.profile)
    else:
        user.profile.likes.add(liked_user.profile)
    return measure(request, id=request.user.id)

def hate(request, id):
    user = request.user
    hated_user = get_object_or_404(User, pk=id)
    is_hater = user.profile in hated_user.profile.haters.all()
    if is_hater:
        user.profile.hates.remove(hated_user.profile)
    else:
        user.profile.hates.add(hated_user.profile)
    return measure(request, id=request.user.id)