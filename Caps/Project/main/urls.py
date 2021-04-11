from django.urls import path, include
from . import views

app_name ='main'
urlpatterns=[
   
    path('calendar/', views.showcalendar, name='calendar'),
]