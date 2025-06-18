from . models import Project, Review, Tag
from django import forms


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'image', 'description', 'source_link']
