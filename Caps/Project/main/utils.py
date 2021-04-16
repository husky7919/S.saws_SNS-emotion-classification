from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Posting

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):
		events_per_day = events.filter(pub_date__day=day)
		d = ''
        
		for event in events_per_day :
			if event.emotion == "행복" :
				d += f'<li>😄</li>'
			elif event.emotion == "완전 기쁨" :
				d += f'<li>😆</li>' 
			elif event.emotion == "분노":
				d += f'<li>😡</li>'	
			elif event.emotion == "슬픔":
				d += f'<li>😢</li>'
			elif event.emotion == "우울":
				d += f'<li>😔</li>'
			elif event.emotion == "평범":
				d += f'<li>🙂</li>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr>{week}</tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):

		events = Posting.objects.filter(pub_date__year=self.year, pub_date__month=self.month)

		cal = f'<table border="1" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal

		