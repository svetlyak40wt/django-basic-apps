from django.shortcuts import render_to_response
from django.http import Http404
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.template import RequestContext
from django.core.mail import send_mail
from django.utils.encoding import smart_unicode

from basic.remarks.models import Remark, RemarkForm, Ban

import re
import md5


def post_remark(request):
  """ Post remark """
  if not request.POST:
    raise Http404, "Only POSTs are allowed"
  
  try:
    target, security_hash = request.POST['target'], request.POST['gonzo']
  except KeyError:
    raise Http404, "One or more of the required fields wasn't submitted"
  
  if md5.new(target + settings.SECRET_KEY).hexdigest() != security_hash:
    raise Http404, "Somebody tampered with the remark form (security violation)"

  content_type_id, object_id = target.split(':')
  content_type = ContentType.objects.get(pk=content_type_id)
  try:
    obj = content_type.get_object_for_this_type(pk=object_id)
  except ObjectDoesNotExist:
    raise Http404, "The remark form had an invalid 'target' parameter -- the object ID was invalid"
  
  new_remark = request.POST.copy()
  new_remark['object_id'] = obj.id
  new_remark['content_type'] = content_type.id
  new_remark['ip_address'] = request.META['REMOTE_ADDR']
  
  # Check for banned users. If there is a match
  # Set status to 'Removed'
  ban_list = Ban.objects.all()
  if ban_list:
    for ban in ban_list:
      m = re.search(ban.rule, request.META['REMOTE_ADDR'])
      if m:
        new_remark['status'] = 3
      else:
        new_remark['status'] = 2
  else:
    new_remark['status'] = 2
  
  remark = Remark()
  form = RemarkForm(new_remark)
  
  if form.is_valid():
    new_remark = form.save()
    context = { 'object':new_remark }
    send_mail('', 'Comment made.', '', settings.MANAGERS_SMS, fail_silently=True)
    return render_to_response('remarks/posted.html', context, context_instance=RequestContext(request))
  else:
    context = {
      'remark': new_remark,
      'remark_form': form,
      'target': target,
      'hash': security_hash,
    }
    return render_to_response('remarks/preview.html', context, context_instance=RequestContext(request))


def remark_was_posted(request):
  """ Display "remark was posted" page """
  if request.GET.has_key('c'):
    content_type_id, object_id = request.GET['c'].split(':')
    try:
      content_type = ContentType.objects.get(pk=content_type_id)
      obj = content_type.get_object_for_this_type(pk=object_id)
      context = { 'object': obj }
    except ObjectDoesNotExist:
      context = {}
  return render_to_response('remarks/posted.html', context, context_instance=RequestContext(request))


def remark_list(request):
  return list_detail.object_list(
    request,
    queryset = Remark.objects.published(),
    paginate_by = 20,
  )