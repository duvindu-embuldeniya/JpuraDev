from django.urls import path
from . views import *

urlpatterns = [
    path('', home, name = 'home'),
    path('projects/', projects, name = 'projects'),

    path('project/<int:id>/', project, name = 'project'),
    path('project-create/', project_create, name = 'project-create'),
    path('project-update/<int:id>/', project_update, name = 'project-update'),
    path('project-delete/<int:id>/', project_delete, name = 'project-delete'),

    path('profile/<str:username>/', profile, name = 'profile'),
]