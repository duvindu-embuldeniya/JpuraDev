from . models import Project, Review, Tag
from django import forms


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'image', 'description', 'source_link']
    
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        # self.fields['title'].widget.attrs.update({'placeholder':'title'})

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
