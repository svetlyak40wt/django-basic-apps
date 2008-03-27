from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from basic.remarks.models import Remark

class RemarkFeed(Feed):
  _site = Site.objects.get_current()
  title = '%s remarks feed' % _site.name
  link = '/remarks/'
  description = '%s remark feed.' % _site.name

  def items(self):
    return Remark.objects.published().order_by('-submit_date')[:10]
    
  def item_pubdate(self, item):
    return item.submit_date