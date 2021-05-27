from django.urls import path, include
from . import views

app_name = "main"
urlpatterns = [
    path("calendar/", views.showcalendar, name="calendar"),
    path("chart/", views.chart, name="chart"),
    path("recommend/", views.reco_music, name="recommend"),
    path("analysis/", views.analysis, name="analysis"),
]
