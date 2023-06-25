from django.shortcuts import render, redirect, get_object_or_404 
# render: 템플릿 불러옴 / redirect: url로 이동 / get_object_or_404: 객체가 있으면 가져오고 없으면 404에러 띄우기
from .models import *
from django.utils import timezone #django 기본 제공 시간관련 기능
from django.db.models import Q #검색창 데이터베이스 활용
from django.views.generic import View, ListView #제네릭뷰 사용
import openpyxl #엑셀파일 사용을 위해 설치

def mainpage(request):
    posts = Post.objects.all() #변수 posts에 Post의 모든 객체 내용을 저장
    return render(request, 'main/mainpage.html', {'posts':posts}) # Read 기능 위한 작업

def firstpage(request):
    return render(request, 'main/firstpage.html')


def secondpage(request):
    return render(request, 'main/secondpage.html')

def thirdpage(request):
    return render(request, 'main/thirdpage.html')

def new(request): #앞의 new.html을 띄우는 함수
    return render(request, 'main/new.html')

def create(request): #포스트 생성(CRUD 중 C)
    if request.user.is_authenticated:
        new_post = Post()
        new_post.title = request.POST['title']
        new_post.writer = request.user
        new_post.pub_date = timezone.now()
        new_post.body = request.POST['body']
        new_post.describe = request.POST['describe']
        new_post.image = request.FILES.get('image')
        
        new_post.save()
        
        return redirect('main:detail', new_post.id) #새로 생성한 post id와함께 detail 페이지로 이동
    else :
        return redirect('accounts:login')

def detail(request, id): #id에 원하는 게시글의 id 값을 넣어 detail 함수를 실행
    post = get_object_or_404(Post, pk = id) #Post와 id를 받아서 전송 or 오류표시
    if request.method == "GET":
        comments = Comment.objects.filter(post=post)
        return render(request, 'main/detail.html', {
            'post':post,
            'comments':comments
        }) # id에 부합하는 게시물 1개씩 관리(detail 페이지)
    # pk(Primary Key): 각 객체를 구분해주는 키 값
    elif request.method == "POST":
        new_comment = Comment()
        new_comment.post = post
        new_comment.writer = request.user
        new_comment.content = request.POST['content']
        new_comment.pub_date = timezone.now()
        new_comment.save()
        return redirect('main:detail', id)
    
def edit(request, id):
    edit_post = Post.objects.get(id=id)
    return render(request, 'main/edit.html', {'post': edit_post})

def update(request, id):
    if request.user.is_authenticated:
        update_post = Post.objects.get(id=id)
        if request.user == update_post.writer:
            update_post.title = request.POST['title']
            update_post.writer = request.user
            update_post.pub_date = timezone.now()
            update_post.body = request.POST['body']
            update_post.describe = request.POST['describe']
            update_post.image = request.FILES.get('image')
            
            update_post.save()
            return redirect('main:detail', update_post.id)
    return redirect('accounts:login')

def delete(request, id):
    delete_post = Post.objects.get(id=id)
    delete_post.delete()
    return redirect('main:mainpage')

from django.shortcuts import render, redirect
from .models import Question, Choice, TestResult

def teamtest1(request):
    if request.method == 'POST':
        scores = request.session.get('scores', {})
        question_id = request.session.get('question_id')
        choice_id = int(request.POST.get(f'question_{question_id}'))
        choice = Choice.objects.get(id=choice_id)
        scores[choice.question.id] = scores.get(choice.question.id, 0) + choice.score

        question = Question.objects.exclude(id__in=scores.keys()).first()
        if question is None:
            # 결과 계산
            result = teamtest2(scores)

            # 결과 저장
            test_result = TestResult.objects.create(result_text=result['result_text'], personality_type=result['personality_type'])

            # 세션 초기화
            request.session['scores'] = None
            request.session['question_id'] = None

            return redirect('main:result', test_result_id=test_result.id)
        else:
            request.session['scores'] = scores
            request.session['question_id'] = question.id

            return redirect('main:teamtest1')
    else:
        if 'scores' not in request.session or 'question_id' not in request.session:
            request.session['scores'] = {}
            request.session['question_id'] = Question.objects.first().id

        question = Question.objects.get(id=request.session['question_id'])
        choices = Choice.objects.filter(question=question)
        context = {'question': question, 'choices': choices}
        return render(request, 'main/teamtest1.html', context)
 

def teamtest2(scores):
    # 각 질문의 점수에 따라 결과 계산
    # 이 예시에서는 간단하게 점수 합계에 따라 결과를 반환하도록 구현
    total_score = sum(scores.values())

    if total_score <= 5:
        result_text = '당신은 "열정적인 리더"입니다. 팀플을 시작해보세요'
        personality_type = "Type A"
    elif total_score <= 10:
        result_text = '당신은 "논리적인 발표자"입니다. 팀플을 시작해보세요'
        personality_type = "Type B"
    else:
        result_text = '당신은 "꼼꼼한 탐정"입니다. 팀플을 시작해보세요'
        personality_type = "Type C"

    return {'result_text': result_text, 'personality_type': personality_type}


def result(request, test_result_id):
    test_result = get_object_or_404(TestResult, id=test_result_id)
    return render(request, 'main/result.html', {'result': test_result})

def maketeam1(request): #글쓰기 페이지 입장 전
    return render(request, 'main/maketeam1.html')

def maketeam2(request): #글쓰기 페이지
    return render(request, 'main/maketeam2.html')




class SearchView(ListView): #검색창
    model = Post
    context_object_name = 'search_results'
    template_name = 'main/search_results.html'
    paginate_by = 8
    
    #모든 리뷰가 아닌, 검색결과에 해당하는 리뷰만 보여줌(get_queryset활용)
    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return Post.objects.filter( #OR조건으로 검색어 필터
            Q(title__icontains=query) #제목에 있거나
            | Q(body__icontains=query) #포스트 내용에 있거나
        )
    
    def get_context_data(self, **kwargs): #템플릿에 검색어 전달
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        return context
    

