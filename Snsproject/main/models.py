from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Posting(models.Model):
    insta = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.TextField(verbose_name="게시글")
    emotion = models.CharField(max_length=30, verbose_name="감정정보", null=True)
    pub_date = models.DateField()

    def __str__(self):
        return "%s %s" % (self.insta, self.emotion)

    def get_absolute_url(self):
        url = reverse("main:detail", args=[str(self.id)])
        return f'<a href="%s">' % (url)


class MusicBox(models.Model):
    emoti = models.CharField(max_length=30, verbose_name="emotion name")
    m_name = models.CharField(max_length=100, verbose_name="music name")
    m_artist = models.CharField(max_length=100, verbose_name="music artist")
    url = models.URLField("URL", unique=True)

    def __str__(self):
        return "%s %s" % (self.emoti, self.music)
