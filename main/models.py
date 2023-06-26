from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200) #제목 필드
    writer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    pub_date = models.DateTimeField() #작성 시간 필드
    body = models.TextField() #팀플 기본적 정보 필드
    describe = models.TextField(blank=True, null=True) #주제 설명 필드
    image = models.ImageField(upload_to="blog/", blank=True, null=True) #이미지 필드
    propensity = models.TextField(blank=True, null=True)
    url = models.TextField(blank=False)
    
    def __str__(self):
        return self.title #데이터를 호출하면 대푯값으로 데이터의 title이 나오게 됨
    
    def summary(self):
        return self.body[:30] #내용이 너무길 때 앞부분 30글자만 보이도록 slicing
    
class Comment(models.Model):
    content = models.TextField()
    pub_date = models.DateTimeField()
    writer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title + " : " + self.content[:20]

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    score = models.IntegerField()

class TestResult(models.Model):
    result_text = models.CharField(max_length=200)
    personality_type = models.CharField(max_length=10)

class Volunteer(models.Model):
    STATUS_CHOICES = [
        ('pending', '팀플 생성자가 승인 여부를 결정하지 못했어요!!'),
        ('accepted', '승인'),
        ('rejected', '팀플 생성자가 승인을 거부했습니다.\n다른 팀플을 찾아보세요!!'),
    ]

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    info = models.CharField(max_length=10, choices=STATUS_CHOICES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)