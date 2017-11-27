from rest_framework import generics, permissions
from rest_framework.response import Response

from member.serializers import UserSerializer
from .pagination import CustomLargePagination
from utils.permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer
from .models import Post


class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly)

    pagination_class = CustomLargePagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly)


class PostLikeView(generics.GenericAPIView):
    queryset = Post.objects.all()

    def post(self, request, *args, **kwargs):
        user = request.user
        post = self.get_object()
        filtered_like_posts = user.like_posts.filter(pk=post.pk)
        if filtered_like_posts.exists():
            user.like_posts.remove(post)
            like_status = False
        else:
            user.like_posts.add(post)
            like_status = True
        data = {
            'user': UserSerializer(user).data,
            'post': PostSerializer(post).data,
            'result': like_status,
        }
        return Response(data)