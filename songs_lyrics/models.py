from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Song(models.Model):
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="creator", default=1)
    name = models.CharField(max_length=100, default="Untitled")
    lyrics = models.CharField(max_length=10000)
    singer1 = models.CharField(max_length=100, blank=True)
    singer2 = models.CharField(max_length=100, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    taal = models.CharField(max_length=100, blank=True)
    link = models.CharField(max_length=300, blank=True)
    album = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=100, blank=True)
    topic = models.CharField(max_length=100, blank=True)
    favorite = models.ManyToManyField(User, blank=True, related_name="favorites")
    likes = models.ManyToManyField(User, blank=True, related_name="likes")


