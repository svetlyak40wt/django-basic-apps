from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from django.views.generic import list_detail
from django.contrib.auth.models import User
from basic.profiles.models import Profile


def profile_list(request):
  return list_detail.object_list(
    request,
    queryset = Profile.objects.all(),
    paginate_by = 20,
  )
profile_list.__doc__ = list_detail.object_list.__doc__


def profile_detail(request, username):
  try:
    user = User.objects.get(username__iexact=username)
  except User.DoesNotExist:
    raise Http404
  
  profile = Profile.objects.get(user=user)
  context = { 'object':profile }
  return render_to_response('profiles/profile_detail.html', context, context_instance=RequestContext(request))