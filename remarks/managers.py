from django.db.models import Manager


class ManagerWithPublished(Manager):
  """ Same as above but for more for templates """
  def published(self):
    return self.get_query_set().filter(status=2)