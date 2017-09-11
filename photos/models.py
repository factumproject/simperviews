""" Models for photos application
"""
from django.db import models


class Album(models.Model):
    """ Album - Stores a collection of photos across years, months, and days
    """
    id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=1024)
    created = models.DateTimeField()

    def __str__(self):
        return self.title


class Photo(models.Model):
    """ Photo
    """
    id = models.UUIDField(primary_key=True)
    file_name = models.CharField(max_length=1024)
    caption = models.CharField(max_length=1024)
    created = models.DateTimeField()
    
    def __str__(self):
        return self.caption


class AlbumPhoto(models.Model):
    """ AlbumPhoto links the photos to the album
    """
    album = models.ForeignKey(Album, on_delete=None)
    photo = models.ForeignKey(Photo, on_delete=None)
    created = models.DateTimeField()
