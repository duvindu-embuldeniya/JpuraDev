from django.urls import path
from . views import *

urlpatterns = [
    path('', home, name = 'home'),
    path('project/<int:pk>/', project, name = 'project'),
]