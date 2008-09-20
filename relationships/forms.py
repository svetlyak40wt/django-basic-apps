from django import forms
from django.forms import ModelForm
from basic.relationships.models import *


class RelationshipForm(ModelForm):
    class Meta:
        model = Relationship