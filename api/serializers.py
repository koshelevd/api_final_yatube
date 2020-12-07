"""Serializers of the 'api' app."""
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    """
    'ModelSerializer' for 'models.Post' objects.
    """
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        """Adds meta-information."""

        # здесь не можем воспользоваться fields = '__all__', так как
        # в документации Redoc явно указаны поля, которые необходимо
        # вернуть, поля 'group' и 'image' в ответ не включаются.
        exclude = ('group', 'image')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """
    'ModelSerializer' for 'models.Comment' objects.
    """

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        """Adds meta-information."""

        fields = '__all__'
        read_only_fields = ('author', 'post')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    """
    'ModelSerializer' for 'models.Group' objects.
    """

    class Meta:
        """Adds meta-information."""

        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    """
    'ModelSerializer' for 'models.Follow' objects.
    """
    user = serializers.SlugRelatedField(slug_field='username',
                                    read_only=True,
                                    default=serializers.CurrentUserDefault())
    following = serializers.SlugRelatedField(slug_field='username',
                                             queryset=User.objects.all())

    class Meta:
        """Adds meta-information."""
        fields = '__all__'
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message='User already follows this author'
            )
        ]

    def validate_following(self, value):
        """
        Validate if 'following' field is not empty or not equals to current
        user.
        """
        if value == '':
            raise serializers.ValidationError('Following is empty')
        if value == self.context['request'].user:
            raise serializers.ValidationError('Can not follow yourself')
        return value
