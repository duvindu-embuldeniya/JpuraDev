from django.shortcuts import render
from django.http import HttpResponse
from . models import Project, Review, Tag



def home(request):
    projects = Project.objects.all()
    context = {'projects':projects}
    return render(request, 'home/index.html', context)


def project(request, pk):
    project = Project.objects.get(id = pk)
    reviews = project.review_set.all()
    tags = project.tag_set.all()
    context = {'project':project, 'reviews':reviews, 'tags':tags}
    return render(request, 'home/project.html', context)