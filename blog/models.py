from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from tagging.fields import TagField
from basic.blog.managers import *

import tagging


class Category(models.Model):
  """ Category """
  title       = models.CharField(_('title'), max_length=100)
  slug        = models.SlugField(_('slug'), prepopulate_from=('title',), unique=True)
  
  class Meta:
    verbose_name = _('category')
    verbose_name_plural = _('categories')
    db_table = 'blog_categories'
    ordering = ('title',)
  
  class Admin:
    pass
  
  def __unicode__(self):
    return u"%s" % self.title
  
  @permalink
  def get_absolute_url(self):
    return ('blog_category_detail', None, { 'slug':self.slug })


class Post(models.Model):
  """ Post model """
  STATUS_CHOICES = (
    (1, _('Draft')),
    (2, _('Public')),
  )
  title           = models.CharField(_('title'), max_length=200)
  slug            = models.SlugField(_('slug'), prepopulate_from=('title',))
  author          = models.ForeignKey(User, blank=True, null=True)
  body            = models.TextField(_('body'))
  tease           = models.TextField(_('tease'), blank=True)
  status          = models.IntegerField(_('status'), choices=STATUS_CHOICES, radio_admin=True, default=2)
  allow_comments  = models.BooleanField(_('allow comments'), default=True)
  publish         = models.DateTimeField(_('publish'))
  created         = models.DateTimeField(_('created'), auto_now_add=True)
  modified        = models.DateTimeField(_('modified'), auto_now=True)
  categories      = models.ManyToManyField(Category, blank=True)
  tags            = TagField()
  objects         = ManagerWithPublished()
  
  class Meta:
    verbose_name = _('post')
    verbose_name_plural = _('posts')
    db_table  = 'blog_posts'
    ordering  = ('-publish',)
    get_latest_by = 'publish'

  class Admin:
    list_display  = ('title', 'publish', 'status')
    list_filter   = ('publish', 'categories', 'status')
    search_fields = ('title', 'body')

  def __unicode__(self):
    return u"%s" % self.title

  @permalink
  def get_absolute_url(self):
      return ('blog_detail', None, {
        'year'  : self.publish.year,
        'month' : self.publish.strftime('%b').lower(),
        'day'   : self.publish.day,
        'slug'  : self.slug
      })