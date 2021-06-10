from django.urls import path
from rest_framework.generics import CreateAPIView
from .views import ListCreateMovieView, RetrieveDestroyMovieView, CreateReviewView, CreateCommentView

urlpatterns = [
    path('movies/', ListCreateMovieView.as_view()),
    # Exemplo de rota utilizando o pk
    #path('movies/<int:pk>/', RetrieveDestroyMovieView.as_view())
    path('movies/<movie_id>/', RetrieveDestroyMovieView.as_view()),
    path('movies/<movie_id>/review/', CreateReviewView.as_view()),
    path('movies/<movie_id>/comments/', CreateCommentView.as_view())

]
