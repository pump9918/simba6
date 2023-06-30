from django.shortcuts import render, redirect, get_object_or_404 
# render: 템플릿 불러옴 / redirect: url로 이동 / get_object_or_404: 객체가 있으면 가져오고 없으면 404에러 띄우기
from .models import *
from django.utils import timezone #django 기본 제공 시간관련 기능
from django.db.models import Q #검색창 데이터베이스 활용
from django.views.generic import View, ListView #제네릭뷰 사용
from excelDB.excel_db import ExcelDB

def mainpage(request):
    posts = Post.objects.all() 
    return render(request, 'main/mainpage.html', {'posts': posts,})

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
        new_post.propensity = request.POST.get('propensity')
        new_post.url = request.POST.get('url')
        
        new_post.save()
        #태그형식
        words = new_post.body.split(' ')
        tag_list = []
        for w in words:
            if len(w)>0:
                if w[0] == '#':
                    tag_list.append(w[1:])
        for t in tag_list:
            tag, boolean = Tag.objects.get_or_create(name=t) 
            new_post.tags.add(tag.id)
        
        return redirect('main:detail', new_post.id) #새로 생성한 post id와함께 detail 페이지로 이동
    else :
        return redirect('accounts:login')

def detail(request, id): #id에 원하는 게시글의 id 값을 넣어 detail 함수를 실행
    post = get_object_or_404(Post, pk = id) #Post와 id를 받아서 전송 or 오류표시
    if request.method == "GET":
        comments = Comment.objects.filter(post=post)
        volunteer = Volunteer.objects.filter(user=request.user, post=post).first
        tags = Tag.objects.all()
        return render(request, 'main/detail.html', {
            'post':post,
            'comments':comments,
            'volunteer': volunteer,
            'tags' : tags,
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
        update_tags = Tag.objects.filter(posts=update_post)
        if request.user == update_post.writer:
            update_post.title = request.POST['title']
            update_post.writer = request.user
            update_post.pub_date = timezone.now()
            update_post.body = request.POST['body']
            update_post.describe = request.POST['describe']
            update_post.image = request.FILES.get('image')
            #태그
            update_tags.delete()
            words = update_post.body.split(' ')
            tag_list = []
            for w in words:
                if len(w)>0:
                    if w[0] == '#':
                        tag_list.append(w[1:])
            for t in tag_list:
                tag, boolean = Tag.objects.get_or_create(name=t)
                update_post.tags.add(tag.id)
            update_post.save()
            
            return redirect('main:detail', update_post.id)
    return redirect('accounts:login')

def delete(request, id):
    delete_post = Post.objects.get(id=id)
    delete_post.delete()
    return redirect('main:mainpage')

# 모든 tag 리스트를 볼 수 있는 페이지 구현
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'main/tag_list.html', {
        'tags':tags,
    })


# 태그 선택 시 해당 태그가 포함된 게시물 보는 기능 구현
def tag_posts(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    posts = tag.posts.all()
    return render(request, 'main/tag_posts.html', {
        'tag':tag,
        'posts':posts,
    })
    
def teamtest1(request):
    if request.method == 'POST':
        user = request.user  # 사용자 정보 가져오기

        scores = request.session.get(f'scores_{user.id}', {})  # 사용자별로 세션 데이터 유지
        question_id = request.session.get(f'question_id_{user.id}')
        choice_id = int(request.POST.get(f'question_{question_id}'))
        choice = Choice.objects.get(id=choice_id)
        scores[choice.question.id] = scores.get(choice.question.id, 0) + choice.score

        question = Question.objects.exclude(id__in=scores.keys()).first()
        if question is None:
            # 결과 계산
            result = teamtest2(scores)

            # 결과 저장
            test_result = TestResult.objects.create(
                user=user,  # 현재 로그인한 사용자 정보 저장
                result_text=result['result_text'],
                personality_type=result['personality_type']
            )

            # 세션 초기화
            request.session[f'scores_{user.id}'] = None
            request.session[f'question_id_{user.id}'] = None

            return redirect('main:result', test_result_id=test_result.id)
        else:
            request.session[f'scores_{user.id}'] = scores
            request.session[f'question_id_{user.id}'] = question.id

            return redirect('main:teamtest1')
    else:
        user = request.user  # 사용자 정보 가져오기

        if f'scores_{user.id}' not in request.session or f'question_id_{user.id}' not in request.session:
            request.session[f'scores_{user.id}'] = {}
            request.session[f'question_id_{user.id}'] = Question.objects.first().id

        question = Question.objects.get(id=request.session[f'question_id_{user.id}'])
        choices = Choice.objects.filter(question=question)
        context = {'question': question, 'choices': choices}
        return render(request, 'main/teamtest1.html', context)


def teamtest2(scores):
    total_score = sum(scores.values())

    if total_score <= 5:
        result_text = "열정적인 리더"
        personality_type = "Type A"
    elif total_score <= 10:
        result_text = "논리적인 발표자"
        personality_type = "Type B"
    else:
        result_text = "꼼꼼한 탐정"
        personality_type = "Type C"

    return {'result_text': result_text, 'personality_type': personality_type}


def result(request, test_result_id):
    test_result = TestResult.objects.get(id=test_result_id)
    return render(request, 'main/result.html', {'result': test_result})
    
# def teamtest1(request):
#     if request.method == 'POST':
#         scores = request.session.get('scores', {})
#         question_id = request.session.get('question_id')
#         choice_id = int(request.POST.get(f'question_{question_id}'))
#         choice = Choice.objects.get(id=choice_id)
#         scores[choice.question.id] = scores.get(choice.question.id, 0) + choice.score

#         question = Question.objects.exclude(id__in=scores.keys()).first()
#         if question is None:
#             # 결과 계산
#             result = teamtest2(scores)

#             # 결과 저장
#             test_result = TestResult.objects.create(result_text=result['result_text'], personality_type=result['personality_type'])

#             # 세션 초기화
#             request.session['scores'] = None
#             request.session['question_id'] = None

#             return redirect('main:result', test_result_id=test_result.id)
#         else:
#             request.session['scores'] = scores
#             request.session['question_id'] = question.id

#             return redirect('main:teamtest1')
#     else:
#         if 'scores' not in request.session or 'question_id' not in request.session:
#             request.session['scores'] = {}
#             request.session['question_id'] = Question.objects.first().id

#         question = Question.objects.get(id=request.session['question_id'])
#         choices = Choice.objects.filter(question=question)
#         context = {'question': question, 'choices': choices}
#         return render(request, 'main/teamtest1.html', context)


# def teamtest2(scores):
#     total_score = sum(scores.values())

#     if total_score <= 5:
#         result_text = "열정적인 리더"
#         personality_type = "Type A"
#     elif total_score <= 10:
#         result_text = "논리적인 발표자"
#         personality_type = "Type B"
#     else:
#         result_text = "꼼꼼한 탐정"
#         personality_type = "Type C"

#     return {'result_text': result_text, 'personality_type': personality_type}


# def result(request, test_result_id):
#     test_result = TestResult.objects.get(id=test_result_id)
#     return render(request, 'main/result.html', {'result': test_result})

def maketeam1(request): #글쓰기 페이지 입장 전
    return render(request, 'main/maketeam1.html')

def maketeam2(request): #글쓰기 페이지
    return render(request, 'main/maketeam2.html')




class SearchView(ListView): #검색창
    model = Post
    excel_db = ExcelDB()
    context_object_name = 'search_results'
    template_name = 'main/search_results.html'
    paginate_by = 8
    
    #모든 리뷰가 아닌, 검색결과에 해당하는 리뷰만 보여줌(get_queryset활용)
    def get_queryset(self):
        query = self.request.GET.get('query', '')
        if self.excel_db.check_search(query):
            return Post.objects.filter(
                Q(title__icontains=query)
                | Q(body__icontains=query)
            )
        else:
            return Post.objects.none()  # 빈 쿼리셋 반환
    
    def get_context_data(self, **kwargs): #템플릿에 검색어 전달
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        return context
    

def volunteer(request, id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=id)
        volunteer = Volunteer()
        volunteer.user = request.user
        volunteer.info = 'pending'
        volunteer.post = post
        volunteer.save()
        return redirect('main:detail', id)
    else:
        return redirect('accounts:login')
