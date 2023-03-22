from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register('friends_requests', views.FriendRequestViewSet,
                basename='friends_requests')
app_name = "friend"

urlpatterns = [
    path('', include(router.urls))
]

print(router.urls)