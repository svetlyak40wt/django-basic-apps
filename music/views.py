from django.views.generic import list_detail
from basic.music.models import *


def genre_detail(request, slug):
  return list_detail.object_detail(
    request,
    queryset = Genre.objects.all(),
    slug = slug,
  )

def genre_list(request):
  return list_detail.object_list(
    request,
    queryset = Genre.objects.all(),
    paginate_by = 20,
  )

def label_detail(request, slug):
  return list_detail.object_detail(
    request,
    queryset = Label.objects.all(),
    slug = slug,
  )

def label_list(request):
  return list_detail.object_list(
    request,
    queryset = Label.objects.all(),
    paginate_by = 20,
  )

def band_detail(request, slug):
  return list_detail.object_detail(
    request,
    queryset = Band.objects.all(),
    slug = slug,
  )

def band_list(request):
  return list_detail.object_list(
    request,
    queryset = Band.objects.all(),
    paginate_by = 20,
  )

def album_detail(request, slug):
  return list_detail.object_detail(
    request,
    queryset = Album.objects.all(),
    slug = slug,
  )

def album_list(request):
  return list_detail.object_list(
    request,
    queryset = Album.objects.all(),
    paginate_by = 20,
  )

def track_detail(request, slug):
  return list_detail.object_detail(
    request,
    queryset = Track.objects.all(),
    slug = slug,
  )

def track_list(request):
  return list_detail.object_list(
    request,
    queryset = Track.objects.all(),
    paginate_by = 20,
  )