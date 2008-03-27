from django.conf.urls.defaults import *


urlpatterns = patterns('',
  url(r'^post/$', 
    view    = 'basic.remarks.views.post_remark',
    name    = 'remark_post',
  ),
  url(r'^posted/$',
    view    = 'basic.remarks.views.remark_was_posted',
    name    = 'remark_posted',
  ),
  url(r'^$',
    view    = 'basic.remarks.views.remark_list',
    name    = 'remark_list',
  ),
)