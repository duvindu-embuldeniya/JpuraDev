from . models import Project, Review, Tag
from django import forms


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'source_link']
