from django.views.generic import list_detail
from basic.places.models import *


def city_detail(request, slug):
  return list_detail.object_detail(
    request,
    queryset = City.objects.all(),
    slug = slug,
  )

def city_list(request):
  return list_detail.object_list(
    request,
    queryset = City.objects.all(),
    paginate_by = 20,
  )

def place_type_detail(request, slug):
  return list_detail.object_detail(
    request,
    queryset = PlaceType.objects.all(),
    slug = slug,
  )

def place_type_list(request):
  return list_detail.object_list(
    request,
    queryset = PlaceType.objects.all(),
    paginate_by = 20,
  )

def place_detail(request, slug):
  return list_detail.object_detail(
    request,
    queryset = Place.objects.all(),
    slug = slug,
  )

def place_list(request):
  return list_detail.object_list(
    request,
    queryset = Place.objects.all(),
    paginate_by = 20,
  )