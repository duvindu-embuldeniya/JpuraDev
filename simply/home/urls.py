from django.urls import path
from . views import *

urlpatterns = [
    path('', home, name = 'home'),
    path('projects/', projects, name = 'projects'),

    path('project/<int:pk>/', project, name = 'project'),
    path('project-create/', project_create, name = 'project-create'),
    path('project-update/<int:pk>/', project_update, name = 'project-update'),
    path('project-delete/<int:pk>/', project_delete, name = 'project-delete'),
]