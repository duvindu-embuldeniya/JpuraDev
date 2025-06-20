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
    path('account/<str:username>/', my_account, name = 'my-account'),
    path('profile/<str:username>/update/', my_account_update, name = 'my-account-update'),
    path('profile/<str:username>/delete/', my_account_delete, name = 'my-account-delete'),

]