from django.shortcuts import render, redirect, get_object_or_404 
# render: 템플릿 불러옴 / redirect: url로 이동 / get_object_or_404: 객체가 있으면 가져오고 없으면 404에러 띄우기
from .models import Post, Comment
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
            update_post.image = request.FILES.get('image')
            
            update_post.save()
            return redirect('main:detail', update_post.id)
    return redirect('accounts:login')

def delete(request, id):
    delete_post = Post.objects.get(id=id)
    delete_post.delete()
    return redirect('main:mainpage')


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
    
# class ExcelUploadView(View):
#     def post(self, request):
#         excelFile = request.FILES['file']
        
#         excel = openpyxl.load_workbook(excelFile, data_only = True)
#         work_sheet = excel.worksheets[0]
        
#         all_values = []
#         for row in work_sheet.rows:
#             row_value = []
#             for cell in row:
#                 row_value.append(cell.value)
#             all_values.append(row_value)
            
#         for row in all_values:
#             sample_model = ExcelModel(classid=row[0], 
#                                        classNum=row[1], 
#                                        className=row[2], 
#                                        professor=row[3], 
#                                        time=row[4], 
#                                        classroom=row[5], 
#                                        credit=row[6])
#             sample_model.save()
            
#         response = {'status':1, 'message': '엠셀파일이 정상적으로 업로드 됐습니다.'}
#         return HttpResponse(json.dumbs(response), content_type='application/json')