from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404

from ..forms import PostCommentForm
from ..models import Post, PostComment
from ...member.decorators import login_required

__all__ = (
    'comment_create',
    'comment_delete',
)


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
