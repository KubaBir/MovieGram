from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'core'
router = SimpleRouter()
router.register('movies', views.MoviesViewSet)
router.register('directors', views.DirectorViewSet)
router.register('user_profiles', views.UserProfileViewSet)
router.register('friends-profiles', views.FriendsProfilesViewSet)
router.register('main_page', views.MainPageViewSet)
router.register('comments', views.CommentsViewSet)
router.register('replies', views.ReplyViewSet)
urlpatterns = [
    path('', include(router.urls))
]
