from django.shortcuts import render, redirect, get_object_or_404

from .forms import PostForm, PostCommentForm
from .models import Post, PostComment


def post_list(request):
    # posts = Post.objects.all().exclude(author__isnull=True)
    posts = Post.objects.all()
    context = {
        "posts": posts,
        "comment_form": PostCommentForm,
    }
    return render(request, 'post/post_list.html', context)


def post_create(request):
    if request.method == 'POST':
        # POST요청의 경우 PostForm인스턴스 생성과정에서 request.POST, request.FILES를 사용
        form = PostForm(request.POST, request.FILES)
        # form이 valid한지 검사
        if form.is_valid():
            post = Post.objects.create(photo=form.cleaned_data['photo'])
            return redirect('post:post_detail', post_pk=post.pk)
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
    # post = get_object_or_404(Post.objects.exclude(author__isnull=True), pk=post_pk)
    post = get_object_or_404(Post, pk=post_pk)
    comment_form = PostCommentForm
    context = {
        'post': post,
        'comment_form': comment_form,
    }
    return render(request, 'post/post_detail.html', context)


def post_delete(request, post_pk):
    if request.method == "POST":
        post = Post.objects.get(pk=post_pk)
        post.delete()
    return redirect("post:post_list")


def comment_create(request, post_pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_pk)
        form = PostCommentForm(request.POST)
        if form.is_valid():
            PostComment.objects.create(post=post, content=form.cleaned_data["content"])
            page_next = request.GET.get('next')
            if page_next:
                return redirect(page_next)
        return redirect("post:post_detail", post_pk=post.pk)
    return redirect("post:post_list")


def comment_delete(request, comment_pk):
    if request.method == "POST":
        comment = get_object_or_404(PostComment, pk=comment_pk)
        post = get_object_or_404(Post, pk=comment.post_id)
        comment.delete()
        return redirect("post:post_detail", post_pk=post.pk)
    return redirect("post:post_list")
