from django.shortcuts import render, redirect
from .models import Posting, MusicBox
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.http import HttpResponse, HttpResponseRedirect
from .utils import Calendar
import datetime
import calendar
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.contrib import auth
from .apps import MainConfig

# 캘린더


def showcalendar(request):
    today = get_date(request.GET.get("month", None))
    userr_id = request.session.get("user1")
    prev_month_var = prev_month(today)
    next_month_var = next_month(today)

    cal = Calendar(today.year, today.month)
    html_cal = cal.formatmonth(userr_id, withyear=True)
    result_cal = mark_safe(html_cal)

    context = {
        "calendar": result_cal,
        "prev_month": prev_month_var,
        "next_month": next_month_var,
    }

    return render(request, "main/calendar.html", context)


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return datetime.date(year, month, day=1)
    return datetime.datetime.today()


def prev_month(day):
    first = day.replace(day=1)
    prev_month = first - datetime.timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(day):
    days_in_month = calendar.monthrange(day.year, day.month)[1]
    last = day.replace(day=days_in_month)
    next_month = last + datetime.timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


# 모델 코드
def analysis(request):
    userr_id = request.session.get("user1")
    if userr_id:
        date = (
            Posting.objects.filter(insta=userr_id)
            .values_list("pub_date", flat=True)
            .distinct()
        )
        for i in date:
            oone_post = (Posting.objects.filter(
                insta=userr_id).filter(pub_date__lte=i))
            one_post = oone_post.last()
            sentences = one_post.post
            logitt = MainConfig.modelss
            logit = logitt.emotionR(sentences)
            one_post.emotion = logit
            one_post.save()
    return redirect("main:calendar")


def chart(request):
    labels = ["anger", "fear", "joy", "love", "sadness", "suprise"]
    emoti1, emoti2, emoti3, emoti4, emoti5, emoti6 = 0, 0, 0, 0, 0, 0
    now = timezone.now()
    lastmonth = now - relativedelta(months=1)
    emoti = Posting.objects.exclude(
        pub_date__gte=now).filter(pub_date__gte=lastmonth)
    for x in emoti:
        if x.emotion == "0":
            emoti1 += 1
        if x.emotion == "1":
            emoti2 += 1
        if x.emotion == "2":
            emoti3 += 1
        if x.emotion == "3":
            emoti4 += 1
        if x.emotion == "4":
            emoti5 += 1
        if x.emotion == "5":
            emoti6 += 1

    data = [emoti1, emoti2, emoti3, emoti4, emoti5, emoti6]
    context = {"labels": labels, "data": data,
               "now": now, "lastmonth": lastmonth}

    return render(request, "main/chart.html", context)


# 컨텐츠 추천
def reco_music(request):
    now = timezone.now()
    lastmonth = now - relativedelta(months=1)
    emot = Posting.objects.exclude(
        pub_date__gte=now).filter(pub_date__gte=lastmonth)

    for x in emot:

        if x.emotion == "anger":
            musics = MusicBox.objects.filter(emoti__contains="anger")[:3]

        elif x.emotion == "sadness":
            musics = MusicBox.objects.filter(emoti__contains="sadness")[:3]

        elif x.emotion == "fear":
            musics = MusicBox.objects.filter(emoti__contains="fear")[:3]

        elif x.emotion == "love":
            musics = MusicBox.objects.filter(emoti__contains="love")[:3]

        elif x.emotion == "suprise":
            musics = MusicBox.objects.filter(emoti__contains="suprise")[:3]

        elif x.emotion == "joy":
            musics = MusicBox.objects.filter(emoti__contains="joy")[:3]

    context = {"emot": emot, "musics": musics}
    return render(request, "main/recommend.html", context)
