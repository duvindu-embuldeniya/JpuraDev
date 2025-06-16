from django.shortcuts import render
from django.http import HttpResponse



projectsList = [

{'id': 1, 'title': 'Ecommerce Website', 'description': 'Fully functional ecommerce website' },

{ 'id': 2, 'title': 'Portfolio Website', 'description': 'A personal website to write articles and display work' },

{'id': 3, 'title': 'Social Network', 'description': 'An open source project built by the community' }

]



def home(request):
    context = {'projects':projectsList}
    return render(request, 'home/index.html', context)


def project(request, pk):
    item = None
    for per in projectsList:
        if per['id'] == pk:
            item = per
    context = {'item':item}
    return render(request, 'home/project.html', context)