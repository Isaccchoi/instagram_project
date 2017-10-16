from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import PostForm
from .models import Post, PostComment


def post_list(request):
    posts = Post.objects.all()
    context = {
        "posts": posts
    }
    return render(request, 'post/post_list.html', context)


def post_create(request):
    if request.method == 'POST':
        # POST요청의 경우 PostForm인스턴스 생성과정에서 request.POST, request.FILES를 사용
        form = PostForm(request.POST, request.FILES)
        # form이 valid한지 검사
        if form.is_valid():
            post = Post.objects.create(photo=form.cleaned_data['photo'])
            return HttpResponse(f'<img src="{post.photo.url}">')
    else:
        # GET요청의 경우 PostForm인스턴스를 생성해서 템플릿에 전달
        form = PostForm

    # GET 요청에서 무조건 실행
    # POST 요청에선 form.is_valid()를 통과 하지 못할 경우 실행
    context = {
        "form": form,
    }
    return render(request, 'post/post_form.html', context)


def post_detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    context = {
        'post': post
    }
    return render(request, 'post/post_detail.html', context)


def post_delete(request, post_pk):
    if request.method == "POST":
        post = Post.objects.get(pk=post_pk)
        post.delete()
    return redirect("post:post_list")


def comment_add(request, post_pk):
    if request.method == "POST":
        post = Post.objects.get(pk=post_pk)
        PostComment.objects.create(post=post, content=request.POST.get("content"))
    return redirect("post:post_list")


def comment_delete(request, comment_pk):
    if request.method == "POST":
        try:
            comment = PostComment.objects.get(pk=comment_pk)
        except PostComment.DoesNotExist:
            return redirect("post:post_list")
        comment.delete()
    return redirect("post:post_list")
