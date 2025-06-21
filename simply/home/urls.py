from django.urls import path
from . views import *

urlpatterns = [
    path('', home, name = 'home'),

    path('register/', register, name = 'register'),
    path('login/', login, name = 'login'),
    path('logout/', logout, name = 'logout'),

    path('projects/', projects, name = 'projects'),
    path('project/<int:id>/', project, name = 'project'),
    path('project-create/', project_create, name = 'project-create'),
    path('project-update/<int:id>/', project_update, name = 'project-update'),
    path('project-delete/<int:id>/', project_delete, name = 'project-delete'),

    #what people see
    path('profile/<str:username>/', profile, name = 'profile'),

    #my-account
    path('account-info/<str:username>/', my_account, name = 'my-account'),
    path('account-update/<str:username>/', my_account_update, name = 'my-account-update'),
    path('account-delete/<str:username>/', my_account_delete, name = 'my-account-delete'),

    path('skill-create/', skill_create, name = 'skill-create'),
    path('skill-update/<int:id>/', skill_update, name = 'skill-update'),
    path('skill-delete/<int:id>/', skill_delete, name = 'skill-delete'),

    path('tag-create/<int:id>/', tag_create, name = 'tag-create'),
    path('tag-option/<int:id>/', tag_option, name = 'tag-option'),
    path('tag-update/<int:id>/', tag_update, name = 'tag-update'),
    path('tag-delete/<int:id>/', tag_delete, name = 'tag-delete'),
]