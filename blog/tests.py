"""
>>> from django.test import Client
>>> from basic.blog.models import Post, Category
>>> import datetime

>>> client = Client()

>>> response = client.get('/posts/')
>>> response.status_code
200

>>> response = client.get('/posts/categories/')
>>> response.status_code
200

>>> category = Category(title='Django', slug='django')
>>> category.save()
>>> response = client.get(category.get_absolute_url())
>>> response.status_code
200

>>> post = Post(title='My post', slug='my-post', body='Lorem ipsum dolor sit amet', status=2, publish=datetime.datetime.now())
>>> post.save()
>>> post.categories.add(category)
>>> response = client.get(post.get_absolute_url())
>>> response.status_code
200
"""