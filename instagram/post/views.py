from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404

from member.decorators import login_required
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


@login_required
def post_create(request):
    # if not request.user.is_authenticated:
    #     return redirect('member:login')
    if request.method == 'POST':
        # POST요청의 경우 PostForm인스턴스 생성과정에서 request.POST, request.FILES를 사용
        form = PostForm(request.POST, request.FILES)
        # form이 valid한지 검사
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post:post_list')
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


@login_required
def post_delete(request, post_pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_pk)
        if post.author != request.user:
            raise PermissionDenied
        post.delete()
    return redirect("post:post_list")


@login_required
def comment_create(request, post_pk):
    # if not request.user.is_authenticated:
    #     return redirect('member:login')
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_pk)
        form = PostCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            page_next = request.GET.get('next').strip()
            if page_next:
                return redirect(page_next)
        return redirect("post:post_detail", post_pk=post.pk)
    return redirect("post:post_list")


@login_required
def comment_delete(request, comment_pk):
    next_page = request.GET.get('next', '').strip()
    if request.method == 'POST':
        comment = get_object_or_404(PostComment, pk=comment_pk)
        if comment.author == request.user:
            comment.delete()
            if next_page:
                return redirect(next_page)
            return redirect('post:post_detail', post_pk=comment.post.pk)
        else:
            raise PermissionDenied('작성자가 아닙니다')


@login_required
def post_like_toggle(request, post_pk):
    if request.method == "POST":
        next_page = request.GET.get('next', '').strip()
        user = request.user
        post = get_object_or_404(Post, pk=post_pk)
        filtered_list_posts = request.user.like_posts.filter(pk=post.pk)
        if filtered_list_posts.exists():
            user.like_posts.remove(post)
        else:
            user.like_posts.add(post)
        if next_page:
            return redirect(next_page)
    return redirect('post:post_detail', post_pk=post_pk)
