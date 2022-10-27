from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('movies', views.MoviesViewSet)
router.register('directors', views.DirectorViewSet)
router.register('user-profiles', views.UserProfileViewSet)
router.register('friends-profiles', views.FriendsProfilesViewSet)
router.register('posts', views.PostViewSet)
router.register('comments', views.CommentViewSet)
urlpatterns = [
    path('', include(router.urls))
]
