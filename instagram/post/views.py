from django.shortcuts import render, redirect

from .models import Post, PostComment


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


def post_delete(request, post_pk):
    if request.method == "POST":
        post = Post.objects.get(pk=post_pk)
        post.delete()
    return redirect("post:post_list")


def comment_add(request, post_pk):
    if request.method == "POST":
        post = Post.objects.get(pk=post_pk)
        PostComment.objects.create(post=post, content=request.POST.get("content"))
        print("------------------------------------------")
        return redirect("post:post_list")
    return redirect("post:post_list")


def comment_delete(request, comment_pk):
    if request.method == "POST":
        try:
            comment = PostComment.objects.get(pk=comment_pk)
        except PostComment.DoesNotExist:
            return redirect("post:post_list")
        comment.delete()
    return redirect("post:post_list")
