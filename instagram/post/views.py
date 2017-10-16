from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Post, PostComment

from .forms import PostForm


def post_list(request):
    posts = Post.objects.all()
    context = {
        "posts": posts
    }
    return render(request, 'post/post_list.html', context)


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post.objects.create(photo=form.cleaned_data['photo'])
            return HttpResponse(f'<img src="{post.photo.url}">')
        else:
            return HttpResponse('Form invalid!!!')
    context = {
        "form": PostForm,
    }
    return render(request, 'post/post_form.html', context)


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
