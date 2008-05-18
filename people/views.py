from django.http import Http404
from django.views.generic import list_detail
from basic.people.models import *


def person_type_detail(request, slug):
    return list_detail.object_detail(
        request,
        queryset = PersonType.objects.all(),
        slug = slug,
    )
person_type_detail.__doc__ = list_detail.object_detail.__doc__


def person_type_list(request):
    return list_detail.object_list(
        request,
        queryset = PersonType.objects.all(),
        paginate_by = 20,
    )
person_type_list.__doc__ = list_detail.object_list.__doc__


def person_detail(request, slug):
    return list_detail.object_detail(
        request,
        queryset = Person.objects.all(),
        slug = slug,
    )
person_detail.__doc__ = list_detail.object_detail.__doc__


def person_list(request):
    return list_detail.object_list(
        request,
        queryset = Person.objects.all(),
        paginate_by = 20,
    )
person_list.__doc__ = list_detail.object_list.__doc__


def person_quote_list(request, slug):
    try:
        person = Person.objects.get(slug__iexact=slug)
    except Person.DoesNotExist:
        raise Http404

    return list_detail.object_list(
        request,
        queryset = person.quote_set.all(),
        paginate_by = 20,
        template_name = 'people/person_quote_list.html',
        extra_context = {'person': person},
    )
person_quote_list.__doc__ = list_detail.object_list.__doc__