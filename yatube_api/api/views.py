from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('You do not have permission to edit this post.')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('You do not have permission to delete this post.')
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post_id=self.kwargs['post_id'])

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('You do not have permission to edit this comment.')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('You do not have permission to delete this comment.')
        instance.delete()
