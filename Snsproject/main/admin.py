from django.contrib import admin
from .models import Posting, MusicBox
# Register your models here.

# 감정에 따른 음악


class MusicBoxAdmin(admin.ModelAdmin):
    list_display = ['id', 'emoti', 'm_name', 'm_artist', 'url']


admin.site.register(MusicBox, MusicBoxAdmin)

# 인스타 게시물 크롤링


class PostingAdmin(admin.ModelAdmin):
    list_display = ['id', 'insta', 'post', 'emotion', 'pub_date']


admin.site.register(Posting, PostingAdmin)
