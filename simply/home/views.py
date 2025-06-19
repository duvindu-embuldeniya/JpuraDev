from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Project, Review, Tag, Profile, Skill
from . forms import ProjectForm
from django.contrib import messages
from django.contrib.auth.models import User,auth


def home(request):
    users = User.objects.all()
    context = {'users':users}
    return render(request, 'home/index.html', context)


def projects(request):
    projects = Project.objects.all()
    context = {'projects':projects}
    return render(request, 'home/projects.html', context)


def project(request, id):
    project = Project.objects.get(id = id)
    context = {'project':project}
    return render(request, 'home/project_info.html', context)


def project_create(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            new_project = form.save()
            messages.success(request, "Project Created Successfully!")
            return redirect('project', id = new_project.id)
    context = {'form':form}
    return render(request, 'home/project_create.html', context)


def project_update(request,id):
    project = Project.objects.get(id = id)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            alt_project = form.save()
            messages.success(request, "Project Updated Successfully!")
            return redirect('project', id=alt_project.id)
    context = {'form':form}
    return render(request, 'home/project_update.html', context)


def project_delete(request,id):
    project = Project.objects.get(id = id)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project Deleted Successfully')
        return redirect('home')
    context = {'project':project}
    return render(request, 'home/project_delete.html', context)


def profile(request,username):
    current_user = User.objects.get(username = username)
    projects = current_user.project_set.all()
    top_skills = current_user.skill_set.exclude(description__exact = '')
    mini_skills = current_user.skill_set.filter(description__exact = '')
    context = {'current_user':current_user, 'projects':projects, 'top_skills':top_skills, 'mini_skills':mini_skills}
    return render(request, 'home/profile.html', context)