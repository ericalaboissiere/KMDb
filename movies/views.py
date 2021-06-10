from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveDestroyAPIView, UpdateAPIView
from .models import Movie, Genre, Comments, Criticism
from .serializers import MovieSerializer, CriticismSerializer, CommentSerializer
from rest_framework.authentication import TokenAuthentication
from .permission import AdminPermission, CriticPermission, UserPermission
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.settings import api_settings

import ipdb


# Create your views here.
class MultipleFildLookupMixin:
    def get_queryset(self):
        queryset = self.queryset
        lookup_filter = {}
        for lookup_fild in self.lookup_filds:
            if self.request.data.get(lookup_fild):
                lookup_filter[f'{lookup_fild}__icontains'] = self.request.data.get(
                    lookup_fild)

        queryset = queryset.filter(**lookup_filter)
        return queryset


class ListCreateMovieView(MultipleFildLookupMixin, ListCreateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminPermission]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_filds = ['title']


class RetrieveDestroyMovieView(RetrieveDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminPermission]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_url_kwarg = 'movie_id'


class CreateReviewView(CreateAPIView, UpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [CriticPermission]
    queryset = Movie.objects.all()
    serializer_class = CriticismSerializer
    lookup_url_kwarg = 'movie_id'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # As linhas acima validam o serializer

        try:

            movie = Movie.objects.get(id=kwargs['movie_id'])
            critics = Criticism.objects.filter(
                movie=movie, critic=request.user)

            if len(critics) == 0:
                critics = Criticism.objects.create(
                    stars=request.data["stars"],
                    review=request.data["review"],
                    spoilers=request.data["spoilers"],
                    critic=request.user,
                    movie=movie
                )

                serializer = CriticismSerializer(critics)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

            else:
                return Response({'detail': 'You already made this review'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except ObjectDoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        movie = Movie.objects.get(id=kwargs['movie_id'])
        try:
            critic = Criticism.objects.get(movie=movie, critic=request.user)

        except ObjectDoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        critic.stars = request.data['stars']
        critic.review = request.data['review']
        critic.spoilers = request.data['spoilers']
        critic.save()
        serializer = CriticismSerializer(critic)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class CreateCommentView(CreateAPIView, UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [UserPermission]
    queryset = Movie.objects.all()
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'movie_id'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # As linhas acima validam o serializer

        try:

            movie = Movie.objects.get(id=kwargs['movie_id'])

        except ObjectDoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        comment = Comments.objects.create(
            user=request.user,
            comment=request.data["comment"],
            movie=movie

        )

        serializer = CommentSerializer(comment)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        movie = Movie.objects.get(id=kwargs['movie_id'])
        try:
            comments = Comments.objects.get(
                id=request.data['comment_id'], user=request.user, movie=movie)

        except ObjectDoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        comments.comment = request.data["comment"]
        comments.save()
        serializer = CommentSerializer(comments)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        # ipdb.set_trace()
        return Response(serializer.data)
