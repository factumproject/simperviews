from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.years, name='years'),
    url(r'^album/(?P<album_id>[0-9a-f-]+)',views.album, name='album'),
    url(r'^albums/',views.albums, name='albums'),
    url(r'^photo/(?P<photo_id>[0-9a-f-]+)',views.photo, name='photo'),
    url(r'^(?P<year>\d{4})/$', views.months, name='months'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', views.month, name='month'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', views.day, name='day'),
]