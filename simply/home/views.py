from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Project, Review, Tag
from . forms import ProjectForm
from django.contrib import messages


def home(request):
    projects = Project.objects.all()
    context = {'projects':projects}
    return render(request, 'home/index.html', context)


def project(request, pk):
    project = Project.objects.get(id = pk)

    context = {'project':project}
    return render(request, 'home/project_info.html', context)


def project_create(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            new_project = form.save()
            messages.success(request, "Project Created Successfully!")
            return redirect('project', pk = new_project.pk)
    context = {'form':form}
    return render(request, 'home/project_create.html', context)


def project_update(request,pk):
    project = Project.objects.get(id = pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            alt_project = form.save()
            messages.success(request, "Project Updated Successfully!")
            return redirect('project', pk=alt_project.pk)
    context = {'form':form}
    return render(request, 'home/project_update.html', context)


def project_delete(request,pk):
    project = Project.objects.get(id = pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project Deleted Successfully')
        return redirect('home')
    context = {'project':project}
    return render(request, 'home/project_delete.html', context)