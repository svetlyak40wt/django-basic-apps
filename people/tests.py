"""
>>> from django.test import Client
>>> from basic.people.models import Person, Quote, PersonType

>>> c = Client()
>>> p = Person.objects.get(pk=1)

>>> r = c.get('/people/')
>>> r.status_code
200

>>> r.context[-1]['object_list']
[<Person: Nathan Borror>]

>>> r = c.get('/people/types/')
>>> r.status_code
200
>>> r.context[-1]['object_list']
[<PersonType: Author>, <PersonType: Director>, <PersonType: Musician>]

>>> r = c.get('/people/types/author/')
>>> r.status_code
200
>>> r.context[-1]['object']
<PersonType: Author>

>>> r = c.get('/people/nathan-borror/')
>>> r.status_code
200
>>> r.context[-1]['object']
<Person: Nathan Borror>

>>> r = c.get('/people/quotes/nathan-borror/')
>>> r.status_code
200

"""
__fixtures__ = ['people.yaml']