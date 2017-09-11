from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def album(request, album_id):
    """ album display all the photos in that album
    """
    return HttpResponse("Album")

def albums(request):
    """ album display all the albums
    """
    return HttpResponse("Albums")


def photo(request, photo_id):
    """ album display all the photos in that album
    """
    return HttpResponse("Photo")

def years(request):
    """ years view that shows all the photos years
    """
    return HttpResponse("Years")


def months(request, year):
    """ months view shows all the months that have photos
    """
    return HttpResponse("Months")


def month(request, year, month):
    """ month view shows all the days of the month with photos
    """
    return HttpResponse("Month")


def day(request, year, month, day):
    """ day view that shows all the photos of the day
    """
    return HttpResponse("Day")
