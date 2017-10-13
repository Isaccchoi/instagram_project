from django.shortcuts import render, redirect

from .models import Post


def post_list(request):
    posts = Post.objects.all()
    context = {
        "posts": posts
    }
    return render(request, 'post/post_list.html', context)


def post_add(request):
    if request.method == "POST":
        Post.objects.create(photo=request.FILES['photo'])
        return redirect("post:post_list")

    context = {

    }
    return render(request, 'post/post_form.html', context)
