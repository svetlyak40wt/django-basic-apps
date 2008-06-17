from django.db.models import Manager
import datetime


class PublicManager(Manager):
    """Returns published posts that are not in the future."""
    def __init__(self, *args, **kwargs):
        self.filter_dict = dict(status__gte=2, publish__lte=datetime.datetime.now())
        super(PublicManager, self).__init__(*args, **kwargs)
    
    def get_query_set(self):
        return super(PublicManager, self).get_query_set().filter(**self.filter_dict)
    
    def published(self):
        return self.get_query_set().filter(**self.filter_dict)