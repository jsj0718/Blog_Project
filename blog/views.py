# from djangogirls.blog.forms import PostForm
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required       # 로그아웃 상태에서 접근하면 404 에러를 나타낸다.

# Create your views here.
# render vs redirect : save()의 유무라고 판단

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts' : posts})

def post_detail(request, pk):
    # pk에 해당하는 Post가 없는 경우, 404 Error Page를 띄움.
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post' : post})

@login_required(login_url='/accounts/login/')
def post_new(request):
    # 전송 방식이 POST인 경우
    if request.method == "POST":
        # Form에서 받은 데이터를 PostForm에 전송
        form = PostForm(request.POST)
        # 값이 유효할 때
        if form.is_valid():
            # Form을 저장하는 작업
            post = form.save(commit=False)      # commit=False : 넘겨진 데이터를 바로 Post모델에 저장하지 말라는 의미
            # 작성자를 추가하는 작업
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            # post.pk를 이용해 View(post_detail)에게 전송
            return redirect('post_detail', pk = post.pk)
    # 전송 방식이 그 외인 경우 (e.x. GET)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form' : form})

@login_required(login_url='/accounts/login/')
def post_edit(request, pk):
    # URL로부터 pk 매개변수를 받아서 처리
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        # 수정하고자 하는 글의 Post모델 instance로 가져온다. (pk로 원하는 글을 찾는다.)
        # 폼을 만들 때(이전에 입력한 데이터 값)와 저장할 때 사용하게 된다.
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required(login_url='/accounts/login/')
def post_draft_list(request):
    # published_date_isnull=True로 발행되지 않은 글 목록을 가져온다.
    # order_by('created_date')로 필드에 대해 오름차순 정렬을 수행한다.
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts' : posts})

@login_required(login_url='/accounts/login/')
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required(login_url='/accounts/login/')
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')