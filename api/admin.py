"""Application 'api' admin page configuration."""
from django.contrib import admin


from .models import Post, Comment, Group, Follow


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Manage posts."""

    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
    )
    search_fields = (
        'text',
    )
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Manage Comments."""

    list_display = (
        'pk',
        'text',
        'created',
        'author',
    )
    search_fields = (
        'text',
    )
    list_filter = ('created',)
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Manage groups."""

    list_display = (
        'pk',
        'title',
        'slug',
        'description',
    )
    search_fields = (
        'title',
        'slug',
    )
    empty_value_display = '-пусто-'
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Manage Followers."""

    list_display = (
        'pk',
        'user',
        'following',
    )
    empty_value_display = '-пусто-'