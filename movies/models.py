from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=255)

# Em movie teremos acesso ao criticism por criticism_set por conta da relação 1->n


class Movie(models.Model):
    title = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    launch = models.DateField()
    classification = models.IntegerField()
    synopsis = models.TextField()
    genres = models.ManyToManyField(Genre)


class Comments(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=CASCADE)


class Criticism(models.Model):
    critic = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField()
    review = models.TextField()
    spoilers = models.BooleanField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
