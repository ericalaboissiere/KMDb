from rest_framework import serializers
from .models import Criticism, Movie, Genre, Comments
from django.contrib.auth.models import User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class UserSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class CriticismSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criticism
        fields = ['id', 'critic', 'stars', 'review', 'spoilers']

    stars = serializers.IntegerField(min_value=1, max_value=10)
    critic = UserSetSerializer(read_only=True)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'user', 'comment']
    user = UserSetSerializer(read_only=True)


class MovieSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'duration', 'genres',
                  'launch', 'classification', 'synopsis', 'criticism_set', 'comments_set']

    def create(self, validated_data):
        movie = Movie.objects.get_or_create(
            title=validated_data["title"],
            duration=validated_data["duration"],
            launch=validated_data["launch"],
            classification=validated_data["classification"],
            synopsis=validated_data["synopsis"]
        )[0]

        genres = validated_data['genres']

        for genre in genres:
            genre_create = Genre.objects.get_or_create(**genre)[0]
            movie.genres.add(genre_create)

        return movie

    genres = GenreSerializer(many=True)
    criticism_set = CriticismSerializer(many=True, read_only=True)
    comments_set = CommentSerializer(many=True, read_only=True)
