from . models import Project, Profile, Skill, Tag
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'image', 'description', 'source_link']
    
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        # self.fields['title'].widget.attrs.update({'placeholder':'title'})

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})





class UserRegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})    

    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email = email).exists():
            raise ValidationError("This mail Is Already Taken!")
        return email





class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']
    
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})   
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_user = self.instance

        if User.objects.filter(email = email).exclude(pk = current_user.pk).exists():
            raise ValidationError("This Email Is Already Taken!")
        return email





class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']
    
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})





class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']
    
    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})





class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
    
    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})