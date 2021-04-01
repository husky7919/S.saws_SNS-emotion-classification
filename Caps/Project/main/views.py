from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Calender, Guest
#now = timezone.now()
# Create your views here.



# 달력 일정 표시   
def result(request):
    emoti = Calender.objects.all()
    return render(request, 'main/result.html');

