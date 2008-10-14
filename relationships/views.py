from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import models
from django.core.mail import EmailMessage
from django.conf import settings

Relationship = models.get_model('relationships', 'relationship')


@login_required
def follow(request, to_user_id, template_name='relationships/relationship_add_confirm.html', success_template_name='relationships/relationship_add_success.html', email_template='relationships/follow_email.txt', mimetype='text/html'):
    to_user = get_object_or_404(User, pk=to_user_id)
    from_user = request.user
    
    if request.is_ajax() or request.POST:
        relationship = Relationship(from_user=from_user, to_user=to_user)
        relationship.save()
        
        if not settings.DEBUG:
            context = {
                'from_user': from_user, 
                'to_user': to_user
            }
            subject =  '%s is now following you' % from_user.username
            message = render_to_string(email_template, context)
            email = EmailMessage(subject, message, settings.REPLY_EMAIL, ['%s' % to_user.email])
            email.send(fail_silently=False)
        
        if request.is_ajax():
            context = "{'success': 'Success', 'to_user_id': '%s'}" % (to_user.id)
            return HttpResponse(context, mimetype="application/json")
        else:
            template_name = success_template_name

    context = {'to_user': to_user}
    return render_to_response(template_name, context, context_instance=RequestContext(request), mimetype=mimetype)


@login_required
def stop_follow(request, to_user_id, template_name='relationships/relationship_delete_confirm.html', success_template_name='relationships/relationship_delete_success.html', mimetype='text/html'):
    to_user = get_object_or_404(User, pk=to_user_id)
    from_user = request.user
    
    if request.is_ajax() or request.POST:
        relationship = get_object_or_404(Relationship, to_user=to_user, from_user=from_user)
        relationship.delete()
        
        if request.is_ajax():
            context = "{'success': 'Success', 'to_user_id': '%s'}" % (to_user.id)
            return HttpResponse(context, mimetype="application/json")
        else:
            template_name = success_template_name
    
    context = {'to_user': to_user}
    return render_to_response(template_name, context, context_instance=RequestContext(request), mimetype=mimetype)