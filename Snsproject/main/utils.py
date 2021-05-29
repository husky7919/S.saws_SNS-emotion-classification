from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Posting
from django.contrib.auth.models import User
from django.contrib import auth


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, events):
        events_per_day = events.filter(pub_date__day=day)
        d = ""
        for event in events_per_day:
            if event.emotion == "0":
                d += event.get_absolute_url()+"😡</a>"
            elif event.emotion == "4":
                d += event.get_absolute_url()+"😭</a>"
            elif event.emotion == "1":
                d += event.get_absolute_url()+"😱</a>"
            elif event.emotion == "3":
                d += event.get_absolute_url()+"😍</a>"
            elif event.emotion == "5":
                d += event.get_absolute_url()+"😳</a>"
            elif event.emotion == "2":
                d += event.get_absolute_url()+"😆</a>"

        if day != 0:
            return f"<td valign=top><span class='date'>{day}</span><br> {d} </td>"
        return "<td></td>"

    def formatweek(self, theweek, events):
        week = ""
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f"<tr height=20 bgcolor=#f3f3f3>{week}</tr>"

    def formatmonth(self, userr_id, withyear=True):
        events = Posting.objects.filter(
            pub_date__year=self.year, pub_date__month=self.month).filter(insta=userr_id)

        cal = f'<table class="calendar">\n'
        cal += f"{self.formatmonthname(self.year, self.month, withyear=withyear)}\n"
        cal += f"{self.formatweekheader()}\n"
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f"{self.formatweek(week, events)}\n"
        return cal
