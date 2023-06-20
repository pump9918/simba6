from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200) #제목 필드
    writer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    pub_date = models.DateTimeField() #작성 시간 필드
    body = models.TextField() #게시글 필드
    image = models.ImageField(upload_to="blog/", blank=True, null=True) #이미지 필드
    
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

# class ExcelModel(models.Model):
#     classid = models.IntegerField(null=False)
#     classNum = models.CharField(max_length = 50, null=False)
#     className = models.CharField(max_length = 50, null=False)
#     professor = models.CharField(max_length = 10, null=False)
#     time = models.CharField(max_length = 50, null=False)
#     classroom = models.CharField(max_length = 50, null=True)
#     credit = models.IntegerField(null=True)
    
#     def __str__(self):
#         return self.className + " | " + self.classNum