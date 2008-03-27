from django import template
from django.conf import settings
from django.core import template_loader
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
import re
Post = models.get_model('blog', 'post')
Category = models.get_model('blog', 'category')

register = template.Library()

#
# Get Latest Posts (templatetag)
#
class LatestPosts(template.Node):
  def __init__(self, limit, var_name):
    self.limit = limit
    self.var_name = var_name
  
  def render(self, context):
    posts = Post.objects.published()[:int(self.limit)]
    if (int(self.limit) == 1):
      context[self.var_name] = posts[0]
    else:
      context[self.var_name] = posts
    return ''

@register.tag(name='get_latest_posts')
def do_get_latest_posts(parser, token):
  """
  Gets any number of latest posts and stores them in a varable.
  
  Syntax::
  
    {% get_latest_posts [limit] as [var_name] %}
  
  Example usage::
    
    {% get_latest_posts 10 as latest_post_list %}
  """
  try:
    tag_name, arg = token.contents.split(None, 1)
  except ValueError:
    raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
  m = re.search(r'(.*?) as (\w+)', arg)
  if not m:
    raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
  format_string, var_name = m.groups()
  return LatestPosts(format_string[0], var_name)

#
# Get Blog Categories (templatetag)
#
class BlogCategories(template.Node):
  def __init__(self, var_name):
    self.var_name = var_name
  
  def render(self, context):
    categories = Category.objects.all()
    context[self.var_name] = categories
    return ''

@register.tag(name='get_blog_categories')
def do_get_blog_categories(parser, token):
  """
  Gets all blog categories.
  
  Syntax::
    
    {% get_blog_categories as [var_name] %}
  
  Example usage::
  
    {% get_blog_categories as category_list %}
  """
  try:
    tag_name, arg = token.contents.split(None, 1)
  except ValueError:
    raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
  m = re.search(r'as (\w+)', arg)
  if not m:
    raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
  var_name = m.groups()[0]
  return BlogCategories(var_name)

#
# Render Inlines (filter)
#
@register.filter
def render_inlines(value):
  """
  Renders inlines in a ``Post`` by passing them through inline templates.
  
  Template Syntax::
    
    {{ post.body|render_inlines|markdown }}
  
  Inline Syntax (singular)::
    
      <inline type="<app_name>.<model_name>" id="<id>" class="med_left"></inline>
    
  Inline Syntax (plural)::
  
      <inline type="<app_name>.<model_name>" ids="<id>, <id>, <id>"></inline>
  
  An inline template will be used to render the inline. Templates will be
  locaed in the following maner:
  
    ``inlines/<app_name>_<model_name>.html``
  
  The template will be passed the following context:
    
    ``object``
      An object for the corresponding passed id.
  
  or
  
    ``object_list``
      A list of objects for the corresponding ids.
  
  It would be wise to anticipate both object_list and object unless 
  you know for sure one or the other will only be present.
  """
  try:
    try:
      from BeautifulSoup import BeautifulSoup
    except ImportError:
      from beautifulsoup import BeautifulSoup
  
    soup = BeautifulSoup(value)
    inline_list = soup.findAll('inline')
    inline_context = {}
  
    for inline in inline_list:
      try:
        app_label, model_name = inline['type'].split('.')
        content_type = ContentType.objects.get(app_label=app_label, model=model_name)
        Model = content_type.model_class()
        try:
          inline_class = inline['class']
        except:
          inline_class = ''
          
        try:
          id_list = [int(i) for i in inline['ids'].split(',')]
          object_list = Model.objects.in_bulk(id_list)
          object_list = list(object_list[int(i)] for i in id_list)
          inline_context = template.Context({ 'object_list': object_list, 'settings':settings, 'class':inline_class })
          inline_template = 'inlines/%s_%s.html' % (content_type.app_label, content_type.model)
        except KeyError:
          obj = Model.objects.get(pk=inline['id'])
          inline_context = template.Context({ 'object': obj, 'settings':settings, 'class':inline_class })
          inline_template = 'inlines/%s_%s.html' % (content_type.app_label, content_type.model)
      except template.TemplateDoesNotExist:
        inline_context = {'error':'Template for "%s" does not exist.' % app_label }
        inline_template = 'inlines/missing.html'
      except ContentType.DoesNotExist:
        inline_context = {'error':'Content type does not exist.'}
        inline_template = 'inlines/missing.html'
      except KeyError:
        inline_context = {'error':'Be sure there are both "type" and "id" attributes in the inline tag.'}
        inline_template = 'inlines/missing.html'
      except ValueError:
        inline_context = {'error':'Type "%s" does not exist' % inline['type'] }
        inline_template = 'inlines/missing.html'
      except Model.DoesNotExist:
        inline_context = {'error':'Object does not exist.' }
        inline_template = 'inlines/missing.html'
      
      try:
        if inline_context['error']:
          if settings.DEBUG is True:
            rendered_inline = template_loader.render_to_string(inline_template, inline_context)
            inline.replaceWith(rendered_inline)
          else:
            inline.replaceWith('')
      except:
        rendered_inline = template_loader.render_to_string(inline_template, inline_context)
        inline.replaceWith(rendered_inline)
    return mark_safe(soup)
  except ImportError:
    return mark_safe(value)

render_inlines.is_safe = True


@register.filter
def get_links(value):
  """
  Extracts links from a ``Post`` body represented as anchor tags and returns an iterable list.
  
  Template Syntax::
    
    {{ post.body|markdown|get_links }}
      
  """
  try:
    try:
      from BeautifulSoup import BeautifulSoup
    except ImportError:
      from beautifulsoup import BeautifulSoup
    soup = BeautifulSoup(value)
    return soup.findAll('a')
  except ImportError:
    if settings.DEBUG:
      raise template.TemplateSyntaxError, "Error in 'get_links' filter: BeautifulSoup isn't installed."
    return value
