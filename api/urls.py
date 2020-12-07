from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet


router = DefaultRouter()

router.register('follow', FollowViewSet, basename='follow')
router.register('group', GroupViewSet)
router.register('posts', PostViewSet, basename='posts')
router.register('posts/(?P<post_id>.+)/comments', CommentViewSet,
                basename='comments')


urlpatterns = [
    path('v1/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/', include(router.urls)),
]
