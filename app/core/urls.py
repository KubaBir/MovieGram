from django.urls import include, path
from rest_framework.routers import SimpleRouter
<<<<<<< HEAD

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
=======
router=SimpleRouter()
router.register('movies',views.MoviesViewSet)
router.register('directors',views.DirectorViewSet)
router.register('user-profiles',views.UserProfileViewSet)
router.register('friends-profiles',views.FriendsProfilesViewSet)
router.register('main_page',views.MainPageViewSet)
router.register('comments',views.CommentsViewSet)
router.register('replies',views.ReplyViewSet)
urlpatterns= [
    path('',include(router.urls))
]
>>>>>>> 25_10_branch
