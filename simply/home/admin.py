from django.contrib import admin
from . models import Tag, Project, Review, Profile, Skill, Message

admin.site.register(Tag)
admin.site.register(Project)
admin.site.register(Review)
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Message)