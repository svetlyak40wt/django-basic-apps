from django import template
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

Remark = models.get_model('remarks', 'Remark')

import re
import md5

register = template.Library()


#
# Get Remark Form
#
class RemarkFormNode(template.Node):
  def __init__(self, obj):
    self.obj = obj
  
  def render(self, context):
    content_type = ContentType.objects.get_for_model(context[self.obj])
    context['target'] = '%s:%s' % (content_type.id, context[self.obj].id)
    context['hash'] = md5.new(context['target'] + settings.SECRET_KEY).hexdigest()
    
    form = loader.get_template('remarks/form.html')
    output = form.render(context)
    
    return output

@register.tag(name='get_remark_form')
def do_get_remark_form(parser, token):
  """ 
  Displays a remarks form.
  
  Syntax::
  
    {% get_remark_form for [object] %}
  
  Example usage::
    
    {% get_remark_form for post %}
  """
  try:
    tag_name, arg = token.contents.split(None, 1)
  except ValueError:
    raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
  m = re.search(r'for (\w+)', arg)
  if not m:
    raise template.TemplateSyntaxError, "First argument in %s tag must be 'for'" % token.contents.split()[0]
  obj = m.groups()[0]
  return RemarkFormNode(obj)


#
# Get Remark Count
#
class RemarkCount(template.Node):
  def __init__(self, obj, var_name):
    self.obj = obj
    self.var_name = var_name
  
  def render(self, context):
    content_type = ContentType.objects.get_for_model(context[self.obj])
    count = Remark.objects.filter(content_type__pk=content_type.id, object_id=context[self.obj].id).count()
    context[self.var_name] = count
    return ''

@register.tag(name='get_remark_count')
def do_get_remark_count(parser, token):
  """
  Gets remark count for object.
  
  Syntax::
  
    {% get_remark_count for [object] as [var_name] %}
  
  Example usage::
  
    {% get_remark_count for post as post_count %}
  """
  try:
    tag_name, arg = token.contents.split(None, 1)
  except ValueError:
    raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
  m = re.search(r'for (\w+) as (\w+)', arg)
  if not m:
    raise template.TemplateSyntaxError, "First argument in %s tag must be 'for' and third must be 'as'" % token.contents.split()[0]
  obj = m.groups()[0]
  var_name = m.groups()[1]
  return RemarkCount(obj, var_name)


#
# Get Remark List
#
class RemarkList(template.Node):
  def __init__(self, obj, var_name):
    self.obj = obj
    self.var_name = var_name
  
  def render(self, context):
    content_type = ContentType.objects.get_for_model(context[self.obj])
    remark_list = Remark.objects.filter(content_type__pk=content_type.id, object_id=context[self.obj].id, status=2)
    context[self.var_name] = remark_list
    return ''

@register.tag(name='get_remark_list')
def do_get_remark_list(parser, token):
  """
  Gets remark count for object.
  
  Syntax::
    
    {% get_remark_list for [object] as [var_name] %}
  
  Example usage::
    
    {% get_remark_list for post as remark_list %}
  """
  try:
    tag_name, arg = token.contents.split(None, 1)
  except ValueError:
    raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
  m = re.search(r'for (\w+) as (\w+)', arg)
  if not m:
    raise template.TemplateSyntaxError, "First argument in %s tag must be 'for' and third must be 'as'" % token.contents.split()[0]
  obj = m.groups()[0]
  var_name = m.groups()[1]
  return RemarkList(obj, var_name)


#
# Get user remarks
#
class UserRemarkList(template.Node):
  def __init__(self, user, var_name):
    self.user = user
    self.var_name = var_name
  
  def render(self, context):
    remark_list = Remark.objects.filter(user=context[self.user].id).order_by('-submit_date')
    context[self.var_name] = remark_list
    return ''

@register.tag(name='get_user_remarks')
def do_get_user_remarks(parser, token):
  """
  Get remarks for a particular user.
  
  Syntax::
    
    {% get_user_remarks for [user] as [var_name] %}
  
  Example usage::
    
    {% get_user_remarks for user as remarks_list %}
  """
  try:
    tag_name, arg = token.contents.split(None, 1)
  except ValueError:
    raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
  m = re.search(r'for (\w+) as (\w+)', arg)
  if not m:
    raise template.TemplateSyntaxError, "First argument in %s must be 'for' and third must be 'as'" % token.contents.split()[0]
  obj = m.groups()[0]
  var_name = m.groups()[1]
  return UserRemarkList(obj, var_name)