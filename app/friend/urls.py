from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('friends_requests', views.FriendRequestViewSet,
                basename='friends_requests')
app_name = "friend"

urlpatterns = [
    path('', include(router.urls))
]

print(router.urls)