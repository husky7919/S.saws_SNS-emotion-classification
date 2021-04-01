from django.contrib import admin
from .models import Calender,Guest
# Register your models here.
class CalenderAdmin(admin.ModelAdmin):
    list_display=['id','insta_id','emotion','pub_date']

admin.site.register(Calender,CalenderAdmin)

class GuestAdmin(admin.ModelAdmin):
    list_display=['id','insta']

admin.site.register(Guest, GuestAdmin)
