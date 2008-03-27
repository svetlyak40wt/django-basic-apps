"""
>>> from django.test import Client
>>> from basic.blog.models import Post, Category

>>> c = Client()

>>> r = c.get('/posts/')
>>> r.status_code
200

>>> r = c.get('/posts/categories/')
>>> r.status_code
200
"""