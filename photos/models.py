""" Models for photos application
"""
from django.db import models

class Setting(models.Model):
    """ Settings - stores some key value pairs
    """
    key = models.CharField(max_length=64, unique=True)
    value = models.CharField(max_length=64)


class Album(models.Model):
    """ Album - Stores a collection of photos across years, months, and days
    """
    id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=1024)
    description = models.TextField()

    created = models.DateTimeField()

    def __str__(self):
        return self.title


class Photo(models.Model):
    """ Photo
    """
    id = models.UUIDField(primary_key=True)
    file_name = models.CharField(max_length=64)
    manufacturer = models.CharField(max_length=64)
    model = models.CharField(max_length=64)
    orientation = models.IntegerField()
    software = models.CharField(max_length=64)
    date_time = models.DateTimeField('date and time')
    ycbcr_positioning = models.CharField(max_length=64)
    compression = models.CharField(max_length=64)
    x_resolution = models.DecimalField(max_digits=8, decimal_places=3)
    y_resolution = models.DecimalField(max_digits=8, decimal_places=3)
    resolution_unit = models.CharField(max_length=64)
    exposure_time = models.CharField(max_length=64)
    f_number = models.CharField(max_length=64)
    exposure_program = models.CharField(max_length=64)
    exif_version = models.CharField(max_length=64)
    date_time_original = models.DateTimeField('original date and time')
    date_time_digitized = models.DateTimeField('digitized date and time')
    components_configuration = models.CharField(max_length=64)
    compressed_bits_per_pixel = models.DecimalField(max_digits=8, decimal_places=3)
    exposure_bias = models.DecimalField(max_digits=8, decimal_places=3)
    max_aperture_value = models.DecimalField(max_digits=8, decimal_places=3)
    metering_mode = models.CharField(max_length=64)
    flash = models.CharField(max_length=64)
    focal_length = models.CharField(max_length=64)
    makernote = models.BinaryField()
    flashpix_version = models.CharField(max_length=64)
    pixel_x_dimension = models.IntegerField()
    pixel_y_dimension = models.IntegerField()
    file_source = models.CharField(max_length=64)
    interoperability_index = models.CharField(max_length=64)
    interoperability_version = models.CharField(max_length=64)
    code_page = models.IntegerField()
    used_extension_numbers = models.IntegerField()
    extension_name = models.CharField(max_length=64)
    extension_class_id = models.CharField(max_length=64)
    extension_persistence = models.CharField(max_length=64)
    extension_create_date = models.DateTimeField('extension create date')
    extension_modify_date = models.DateTimeField('extension modify date')
    creating_application = models.CharField(max_length=64)
    extension_description = models.CharField(max_length=64)
    storage_stream_pathname = models.CharField(max_length=64)
    screen_nail = models.CharField(max_length=64)
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
