from django.shortcuts import render
from .models import Posting, MusicBox
from django.db.models import Q
from django.views import generic
from django.utils.safestring import mark_safe
from django.http import HttpResponse, HttpResponseRedirect
from .utils import Calendar
import datetime
import calendar
#import matplotlib.pyplot as plt

def showcalendar(request):

    today = get_date(request.GET.get('month', None))

    prev_month_var = prev_month(today)
    next_month_var = next_month(today)

    cal = Calendar(today.year, today.month)
    html_cal = cal.formatmonth(withyear=True)
    result_cal = mark_safe(html_cal)

    context = {'calendar' : result_cal, 
    'prev_month' : prev_month_var, 
    'next_month' : next_month_var}

    return render(request, 'main/calendar.html', context)

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.datetime.today()

def prev_month(day):
    first = day.replace(day=1)
    prev_month = first - datetime.timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(day):
    days_in_month = calendar.monthrange(day.year, day.month)[1]
    last = day.replace(day=days_in_month)
    next_month = last + datetime.timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def chart(request):
    labels = ['Utter joy', 'Happiness', 'anger','sadness','depressed','normal']
    emoti1 = Posting.objects.filter(emotion__contains='완전 기쁨').count()
    emoti2 = Posting.objects.filter(emotion__contains='행복').count()
    emoti3 = Posting.objects.filter(emotion__contains='분노').count()
    emoti4 = Posting.objects.filter(emotion__contains='슬픔').count()
    emoti5 = Posting.objects.filter(emotion__contains='우울').count()
    emoti6 = Posting.objects.filter(emotion__contains='평범').count()
    data = [emoti1, emoti2, emoti3, emoti4, emoti5, emoti6]
    return render(request, 'main/chart.html', {'labels':labels, 'data':data})






    


