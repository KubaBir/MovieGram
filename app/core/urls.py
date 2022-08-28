from django.urls import path
from . import views
urlpatterns= [
    path('movies/',views.MoviesListView.as_view()),
    path('directors/',views.DirectorListView.as_view()),
    path('user-top/',views.UserTopMoviesListView.as_view())
]