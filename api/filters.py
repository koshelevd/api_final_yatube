"""Filters of the 'api' app."""
from django.shortcuts import get_object_or_404
from rest_framework import filters

from api.models import Group, User


class FilterPostsByGroupBackend(filters.BaseFilterBackend):
    """
    If group id is specified then filter posts by that group.
    """

    def filter_queryset(self, request, queryset, view):
        group_id = request.GET.get('group')
        if group_id is not None:
            group = get_object_or_404(Group, pk=group_id)
            queryset = group.posts.all()
        return queryset


class FilterFollowersBackend(filters.BaseFilterBackend):
    """
    If follower is specified then filter.
    """

    def filter_queryset(self, request, queryset, view):
        follower_username = request.GET.get('search')
        followers = queryset.filter(following=request.user)
        if follower_username is not None:
            follower = get_object_or_404(User, username=follower_username)
            return followers.filter(user=follower)
        return followers
