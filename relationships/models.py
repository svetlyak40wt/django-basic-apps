from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class RelationshipManager(models.Manager):
    def relationships_for_user(self, user):
        relationships = {'friends': [], 'followers': []}
        
        for relationship in self.filter(from_user=user):
            relationships['friends'].append(relationship.to_user)
        
        for relationship in self.filter(to_user=user):
            relationships['followers'].append(relationship.from_user)
        
        return relationships
    
    def relationship(self, from_user, to_user):
        if self.filter(from_user=from_user, to_user=to_user).count() > 0:
            return True
        if self.filter(from_user=to_user, to_user=from_user).count() > 0:
            return True
        return False


class Relationship(models.Model):
    """ Relationship model """
    from_user       = models.ForeignKey(User, related_name='from_users')
    to_user         = models.ForeignKey(User, related_name='to_users')
    created         = models.DateTimeField(auto_now_add=True)
    objects         = RelationshipManager()
    
    class Meta:
        unique_together = (('from_user', 'to_user'),)
        verbose_name = _('relationship')
        verbose_name_plural = _('relationships')
        db_table = 'relationships'

    def __unicode__(self):
        return '<Relationship>'