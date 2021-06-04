from django.shortcuts import render, redirect, get_object_or_404
from .models import MusicBox, Posting
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.http import HttpResponse, HttpResponseRedirect
from .utils import Calendar
import datetime
import calendar
import random
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
    co = 0
    if userr_id:
        date = (
            Posting.objects.filter(insta=userr_id)
            .values_list("pub_date", flat=True)
            .distinct()
        )
        for i in date:
            oone_post = (Posting.objects.filter(
                insta=userr_id).filter(pub_date=i))
            one_post = oone_post.first()
            sentences = one_post.post
            logitt = MainConfig.modelss
            logit = logitt.emotionR(sentences)
            one_post.emotion = logit
            one_post.save()
    return render(request, "main/analysis.html")


def emoti_count(emoti):
    emoti1, emoti2, emoti3, emoti4, emoti5, emoti6 = 0, 0, 0, 0, 0, 0
    data = []
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
    return data


def chart(request):
    userr_id = request.session.get("user1")
    labels = ["anger", "fear", "joy", "love", "sadness", "suprise"]
    now = timezone.now()
    lastmonth = now - relativedelta(months=1)
    emoti = Posting.objects.exclude(
        pub_date__gte=now).filter(pub_date__gte=lastmonth).filter(insta=userr_id)

    data = []
    data = emoti_count(emoti)
    context = {"labels": labels, "data": data,
               "now": now, "lastmonth": lastmonth}
    return render(request, "main/chart.html", context)
# 컨텐츠 추천


def reco_music(request):
    userr_id = request.session.get("user1")
    now = timezone.now()
    lastmonth = now - relativedelta(months=1)
    emoti = Posting.objects.exclude(
        pub_date__gte=now).filter(pub_date__gte=lastmonth).filter(insta=userr_id)

    data = []
    data = emoti_count(emoti)
    max = data[0]
    for i in range(0, 6):
        if data[i] > max:
            max = data[i]
            maxemoti = i

    if maxemoti == 0:
        musics = list(MusicBox.objects.filter(emoti__contains="anger"))
        musics = random.sample(musics, 3)
        emot = "anger"
    elif maxemoti == 4:
        musics = list(MusicBox.objects.filter(emoti__contains="sadness"))
        emot = "sadness"
        musics = random.sample(musics, 3)
    elif maxemoti == 1:
        musics = list(MusicBox.objects.filter(emoti__contains="fear"))
        emot = "fear"
        musics = random.sample(musics, 3)
    elif maxemoti == 3:
        musics = list(MusicBox.objects.filter(emoti__contains="love"))
        emot = "love"
        musics = random.sample(musics, 3)
    elif maxemoti == 5:
        musics = list(MusicBox.objects.filter(emoti__contains="suprise"))
        emot = "suprise"
        musics = random.sample(musics, 3)
    elif maxemoti == 2:
        musics = list(MusicBox.objects.filter(emoti__contains="joy"))
        emot = "joy"
        musics = random.sample(musics, 3)

    context = {"emot": emot, "musics": musics}
    return render(request, "main/recommend.html", context)


def detail(request, pk):
    post_detail = get_object_or_404(Posting, pk=pk)
    return render(request, 'main/detail.html', {'posts': post_detail})
