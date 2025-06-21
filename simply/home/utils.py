from . models import Profile, Skill, Project, Tag
from django.contrib.auth.models import User
from django.db.models import Q


def search_profiles(request):
    query = request.GET.get('query') if request.GET.get('query') else ''

    skills = Skill.objects.filter(
        Q(name__icontains = query)
    )

    users = User.objects.distinct().filter(
        Q(username__icontains = query)|
        Q(profile__name__icontains = query)|
        Q(skill__in = skills)
    )

    return query, users



def search_projects(request):
    query = request.GET.get('query') if request.GET.get('query') else ''

    tags = Tag.objects.filter(
        Q(name__icontains = query)
    )

    projects = Project.objects.distinct().filter(
        Q(title__icontains = query)|
        Q(description__icontains = query)|
        Q(owner__username__icontains = query)|
        Q(owner__profile__name__icontains = query)|
        Q(tag__in = tags)
    )

    return query, projects