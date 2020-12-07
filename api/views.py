"""View classes of the 'api' app."""
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .models import Post, Group, Follow, User
from .serializers import (PostSerializer,
                          CommentSerializer,
                          GroupSerializer,
                          FollowSerializer, )
from .permissions import ResourcePermission, IsAuthenticated
from .filters import FilterPostsByGroupBackend, FilterFollowersBackend


class FollowViewSet(viewsets.ModelViewSet):
    """
    Viewset for 'models.Follow' model.
    """

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (ResourcePermission, IsAuthenticated)
    filter_backends = [FilterFollowersBackend]

    def perform_create(self, serializer):
        """
        Override perform_create function.

        Validate data then save user and following.
        """
        if serializer.is_valid(raise_exception=True):
            following_username = serializer.validated_data['following']
            following = get_object_or_404(User, username=following_username)
            serializer.save(user=self.request.user, following=following)


class GroupViewSet(viewsets.ModelViewSet):
    """
    Viewset for 'models.Group' model.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (ResourcePermission,)


class PostViewSet(viewsets.ModelViewSet):
    """
    Viewset for 'models.Post' model.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (ResourcePermission,)
    filter_backends = [FilterPostsByGroupBackend]

    def perform_create(self, serializer):
        """
        Override perform_create function.

        Save 'author' field.
        """
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Viewset for 'models.Comment' model.
    """

    serializer_class = CommentSerializer
    permission_classes = (ResourcePermission, IsAuthenticated)

    def get_post(self):
        """
        Return 'models.Post' specified in URL by id.
        """
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        """
        Override perform_create function.

        Save 'author' and 'post' fields.
        """
        serializer.save(author=self.request.user,
                        post=self.get_post())

    def get_queryset(self):
        """
        Override get_queryset.

        Return 'models.Comment' queryset for post_id in URL.
        """
        return self.get_post().comments.all()
