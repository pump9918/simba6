from django.db import models
from django.contrib.auth.models import User

class MyTag(models.Model):
    mytagname = models.CharField(max_length=30, null=False, blank=False)
    
    def __str__(self):
        return self.mytagname

class Profile(models.Model): #기존 allauth에서 제공하는건 User에서, 개인적으로 추가하는 필드는 Profile 클래스로
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade = models.IntegerField(default=1)
    department = models.TextField(null=True, max_length=30)
    name = models.TextField(null=True, max_length=10)
    nickname = models.TextField(null=True, max_length=10)
    likes = models.ManyToManyField("self", related_name="likers", symmetrical=False)
    hates = models.ManyToManyField("self", related_name="haters", symmetrical=False)
    userImage = models.ImageField(upload_to="blog/", blank=True, null=True) #이미지 필드
    mytags = models.TextField(null=True, max_length=30)
    taglist = models.ManyToManyField(MyTag, related_name='users', blank=True)
