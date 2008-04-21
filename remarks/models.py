from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.newforms import ModelForm
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from basic.remarks.managers import ManagerWithPublished


class Ban(models.Model):
  """ Ban model """
  BAN_TYPES = (
    ('remark', 'Remark'),
    ('person_name', 'Person Name'),
    ('person_email', 'Person Email'),
    ('person_url', 'Person URL'),
    ('ip_address', 'IP Address'),
  )
  field           = models.CharField(_('field'), max_length=20, choices=BAN_TYPES)
  rule            = models.CharField(_('rule'), blank=True, max_length=100)
  
  class Meta:
    db_table  = 'remarks_bans'
    
  class Admin:
    list_display = ('rule', 'field')
    list_filter = ('field',)
    search_fields = ('rule',)

  def __unicode__(self):
    return self.rule
  

class Remark(models.Model):
  """ Remark model """
  STATUS_CHOICES = (
    (1, 'Pending'),
    (2, 'Public'),
    (3, 'Removed'),
  )
  content_type    = models.ForeignKey(ContentType)
  object_id       = models.PositiveIntegerField()
  content_object  = generic.GenericForeignKey('content_type', 'object_id')
  remark          = models.TextField(_('remark'), max_length=3000)
  user            = models.ForeignKey(User, blank=True, null=True)
  person_name     = models.CharField(_('person name'), max_length=50)
  person_email    = models.EmailField(_('person email'), blank=True)
  person_url      = models.URLField(_('person url'), blank=True, verify_exists=False)
  submit_date     = models.DateTimeField(_('submit date'), auto_now_add=True)
  status          = models.IntegerField(_('status'), choices=STATUS_CHOICES, radio_admin=True, default=2)
  ip_address      = models.IPAddressField(_('ip address'), )
  is_featured     = models.BooleanField(_('is featured'), default=False)
  objects         = ManagerWithPublished()
  
  class Meta:
    db_table = 'remarks'
    ordering = ('submit_date',)
  
  class Admin:
    list_display = ('person_name', 'remark', 'submit_date', 'content_type', 'is_public')
    list_filter   = ('content_type',)
    search_fields = ('remark', 'person_name')
    ordering = ('-submit_date',)
  
  def __unicode__(self):
    return '%s says: %s...' % (self.person_name, self.remark[:100])
  
  def get_absolute_url(self):
    return '%s#c%s' % (self.content_object.get_absolute_url(), self.id)
  
  @property
  def is_removed(self):
    return self.status == 3
  
  @property
  def is_public(self):
    return self.status == 2


class RemarkForm(ModelForm):
  """ Remark form """
  class Meta:
    model = Remark