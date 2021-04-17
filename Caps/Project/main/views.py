from django.shortcuts import render
from .models import Posting, MusicBox
from django.db.models import Q
from django.views import generic
from django.utils.safestring import mark_safe
from django.http import HttpResponse, HttpResponseRedirect
from .utils import Calendar
import datetime
import calendar
from dateutil.relativedelta import relativedelta
from django.utils import timezone

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
    labels = ['완전 기쁨', '행복', '분노','슬픔','우울','평범']
    now =timezone.now()
    lastmonth = timezone.now()-relativedelta(months=1)
    emoti1 = Posting.objects.filter(emotion__contains='완전 기쁨').exclude(pub_date__gte=now).filter(pub_date__gte=lastmonth).count()
    emoti2 = Posting.objects.filter(emotion__contains='행복').exclude(pub_date__gte=now).filter(pub_date__gte=lastmonth).count()
    emoti3 = Posting.objects.filter(emotion__contains='분노').exclude(pub_date__gte=now).filter(pub_date__gte=lastmonth).count()
    emoti4 = Posting.objects.filter(emotion__contains='슬픔').exclude(pub_date__gte=now).filter(pub_date__gte=lastmonth).count()
    emoti5 = Posting.objects.filter(emotion__contains='우울').exclude(pub_date__gte=now).filter(pub_date__gte=lastmonth).count()
    emoti6 = Posting.objects.filter(emotion__contains='평범').exclude(pub_date__gte=now).filter(pub_date__gte=lastmonth).count()
    data = [emoti1, emoti2, emoti3, emoti4, emoti5, emoti6]

    return render(request, 'main/chart.html', {'labels':labels, 'data':data, 'now':now, 'lastmonth':lastmonth})






    


