from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Project, Review, Tag, Profile, Skill, Message
from . forms import (
    ProjectForm, UserRegistrationForm, UserUpdateForm, ProfileUpdateForm,
    SkillForm, TagForm, ReviewForm, MessageForm
    )
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from . utils import search_profiles, search_projects
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



def home(request):
    # objects = User.objects.all()
    
    query,objects = search_profiles(request)
    result = 1

    paginator = Paginator(objects,result)
    page = request.GET.get('page') if request.GET.get('page') else ''

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        page = '1'
        objects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        objects = paginator.page(page)

    context = {'objects':objects, 'query':query}
    return render(request, 'home/index.html', context)




def register(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # new_user = form.save(commit=False)
            # new_user.username = new_user.username.lower()
            # new_user.save()
            new_user = form.save()
            auth.login(request, new_user)
            messages.success(request, "Account Created Successfully!")
            return redirect('home')
    context = {'form':form}
    return render(request, 'home/register.html', context)




def login(request):
    if request.user.is_authenticated:
        messages.info(request, "You've Already Loged-In!")
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        auth_user = auth.authenticate(username = username, password = password)
        if auth_user is not None:
            auth.login(request, auth_user)
            messages.success(request, "Successfully Loged-In!")
            return redirect(request.GET.get('next') if request.GET.get('next') else 'home')
        else:
            messages.error(request, "User Doesn't Exist!")
            return redirect('login')
    return render(request, 'home/login.html')




def logout(request):
    if not(request.user.is_authenticated):
        messages.info(request, "You've Not Logd-In!")
        return redirect('home')
    auth.logout(request)
    messages.success(request, "Successfully Loged-Out!")
    return redirect('home')




def projects(request):
    # projects = Project.objects.all()

    query, objects = search_projects(request)
    result = 1

    paginator = Paginator(objects, result)
    page = request.GET.get('page') if request.GET.get('page') else ''

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        page = '1'
        objects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        objects = paginator.page(page)

    context = {'objects':objects, 'query':query}
    return render(request, 'home/projects.html', context)




def project(request, id):
    project = Project.objects.get(id = id)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_vote = form.save(commit=False)
            new_vote.owner = request.user
            new_vote.project = project
            new_vote.save()
            messages.success(request, "Vote Added Successfully!")
        
            project.update_values

            return redirect('project', id = project.pk)
        
    context = {'project':project, 'form':form}
    return render(request, 'home/project_info.html', context)




@login_required
def project_create(request):
    current_user = request.user
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.owner = request.user
            new_project.save()
            messages.success(request, "Project Created Successfully!")
            return redirect('my-account', username = current_user.username)
    context = {'form':form, 'current_user':current_user}
    return render(request, 'home/project_create.html', context)




@login_required
def project_update(request,id):
    current_user = request.user
    project = Project.objects.get(id = id)
    if request.user != project.owner:
        return HttpResponse('<h1>403 Forbidden!</h1>')
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            alt_project = form.save()
            messages.success(request, "Project Updated Successfully!")
            return redirect('my-account', username = current_user.username)
    context = {'form':form, 'current_user':current_user}
    return render(request, 'home/project_update.html', context)




@login_required
def project_delete(request,id):
    current_user = request.user
    project = Project.objects.get(id = id)
    if request.user != project.owner:
        return HttpResponse('<h1>403 Forbidden!</h1>')
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project Deleted Successfully')
        return redirect('my-account', username = current_user.username)
    context = {'project':project, 'current_user':current_user}
    return render(request, 'home/project_delete.html', context)




#what people see
def profile(request,username):
    current_user = User.objects.get(username = username)
    projects = current_user.project_set.all()
    top_skills = current_user.skill_set.exclude(description__exact = '')
    mini_skills = current_user.skill_set.filter(description__exact = '')
    context = {'current_user':current_user, 'projects':projects, 'top_skills':top_skills, 'mini_skills':mini_skills}
    return render(request, 'home/profile.html', context)




#my-account
@login_required
def my_account(request,username):
    current_user = User.objects.get(username = username)
    if request.user != current_user:
        return HttpResponse('<h1>043 Forbidden!')
    projects = current_user.project_set.all()
    top_skills = current_user.skill_set.exclude(description__exact = '')
    other_skills = current_user.skill_set.filter(description__exact = '')
    context = {'current_user':current_user, 'projects':projects, 'top_skills':top_skills, 'other_skills':other_skills}
    return render(request, 'home/account.html', context)




@login_required
def my_account_update(request,username):
    current_user = User.objects.get(username = username)
    if request.user != current_user:
        return HttpResponse('<h1>043 Forbidden!</h1>')
    u_form = UserUpdateForm(instance=current_user)
    p_form = ProfileUpdateForm(instance=current_user.profile)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance = current_user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=current_user.profile)
        if u_form.is_valid() and p_form.is_valid():
            # alt_user = u_form.save(commit=False)
            # alt_user.username = alt_user.username.lower()
            # alt_user.save()
            alt_user = u_form.save()
            p_form.save()
            messages.success(request, "Account Updated Successfully!")
            return redirect('my-account', username = alt_user.username)
    context = {'current_user':current_user, 'u_form':u_form, 'p_form':p_form}
    return render(request, 'home/account_update.html', context)




@login_required
def my_account_delete(request,username):
    current_user = User.objects.get(username = username)
    if request.user != current_user:
        return HttpResponse('<h1>043 Forbidden!</h1>')
    if request.method == 'POST':
        current_user.delete()
        messages.success(request, "Account Deleted Successfully!")
        return redirect('home')
    context = {'current_user':current_user}
    return render(request, 'home/account_delete.html', context)




@login_required
def skill_create(request):
    current_user = request.user
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            new_skill = form.save(commit=False)
            new_skill.owner = request.user
            new_skill.save()
            messages.success(request, "Skill Created Successfully!")
            return redirect('my-account', username = current_user.username)
    context = {'current_user':current_user, 'form':form}
    return render(request, 'home/skill_create.html', context)




@login_required
def skill_update(request,id):
    current_user = request.user
    skill = Skill.objects.get(id = id)
    if request.user != skill.owner:
        return HttpResponse('<h1>403 Forbidden!</h1>')
    form = SkillForm(instance = skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance = skill)
        if form.is_valid():
            alt_skill = form.save()
            messages.success(request, "Skill Updated Successfully!")
            return redirect('my-account', username = current_user.username)
    context = {'current_user':current_user, 'skill':skill, 'form':form}
    return render(request, 'home/skill_update.html', context)




@login_required
def skill_delete(request, id):
    current_user = request.user
    skill = Skill.objects.get(id = id)
    if request.user != skill.owner:
        return HttpResponse('<h1>403 Forbidden!</h1>')
    if request.method == 'POST':
        skill.delete()
        messages.success(request, "Skill Deleted Successfully!")
        return redirect('my-account', username = current_user.username)
    context = {'current_user':current_user, 'skill':skill}
    return render(request, 'home/skill_delete.html', context)




@login_required
def tag_create(request, id):
    current_user = request.user
    project = Project.objects.get(id = id)
    form = TagForm()
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            new_tag = form.save(commit=False)
            new_tag.project = project
            new_tag.save()
            messages.success(request, "Tag Created Successfully!")
            return redirect('my-account', username = current_user.username)
    context = {'current_user':current_user, 'form':form}
    return render(request, 'home/tag_create.html', context)




@login_required
def tag_option(request, id):
    current_user = request.user
    tag = Tag.objects.get(id = id)
    if current_user != tag.project.owner:
        return HttpResponse('<h1>403 Forbidden!</h1>')
    context = {'tag':tag, 'current_user':current_user}
    return render(request, 'home/tag_option.html', context)




@login_required
def tag_update(request, id):
    tag = Tag.objects.get(id = id)
    current_user = request.user
    if current_user != tag.project.owner:
        return HttpResponse('<h1>403 Forbidden!</h1>')
    form = TagForm(instance = tag) 
    if request.method == 'POST':
        form = TagForm(request.POST, instance = tag)
        if form.is_valid():
            form.save()
            messages.success(request, "Tag Updated Successfully!")
            return redirect('my-account', username = current_user.username)
    context = {'tag':tag, 'form':form, 'current_user':current_user}
    return render(request, 'home/tag_update.html', context)




@login_required
def tag_delete(request,id):
    tag = Tag.objects.get(id = id)
    current_user = request.user
    if current_user != tag.project.owner:
        return HttpResponse('<h1>403 Forbidden!</h1>')
    if request.method == 'POST':
        tag.delete()
        messages.success(request, "Tag Deleted Successfully!")
        return redirect('my-account', username = current_user.username)
    context = {'tag':tag, 'current_user':current_user}
    return render(request, 'home/tag_delete.html', context)




@login_required
def message_create(request, username):
    profile_owner = User.objects.get(username = username)
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_msg = form.save(commit=False)
            new_msg.sender = request.user
            new_msg.receiver = profile_owner
            new_msg.name = request.user.profile.name
            new_msg.email = request.user.email
            new_msg.save()
            messages.success(request, 'Message Created Successfully!')
            return redirect('profile', username = profile_owner.username)
    context = {'form':form, 'profile_owner':profile_owner}
    return render(request, 'home/message_create.html', context)




@login_required
def message_inbox(request,username):
    current_user = User.objects.get(username = username)
    all_messages = current_user.receiver.all()
    new_messages_count = all_messages.filter(is_read = False).count()
    context = {'all_messages':all_messages, 'new_messages_count':new_messages_count}
    return render(request, 'home/message_inbox.html', context)




@login_required
def message_view(request, id):
    msg = Message.objects.get(id = id)
    if request.user != msg.receiver:
        return HttpResponse('<h1>403 Forbidden!</h1>')
    if msg.is_read == False:
        msg.is_read = True
        msg.save()
    context = {'msg':msg}
    return render(request, 'home/message_view.html', context)




@login_required
def message_reply(request, id):
    msg = Message.objects.get(id = id)
    if request.user != msg.receiver:
        return HttpResponse('<h1>403 Forbidden!</h1>')
    sender = request.user
    receiver = msg.sender
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_msg = form.save(commit=False)
            new_msg.sender = sender
            new_msg.receiver = receiver
            new_msg.name = sender.profile.name
            new_msg.email = sender.email
            new_msg.save()
            messages.success(request, "Replied Successfully!")
            return redirect('message-view', id = msg.id)
    context = {'form':form, 'msg':msg}
    return render(request, 'home/message_reply.html', context)