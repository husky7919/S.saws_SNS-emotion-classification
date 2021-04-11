from django.db import models

#from django.utils import timezone

# Create your models here.


class Posting (models.Model):
    insta = models.CharField(max_length=30, verbose_name="인스타 아이디")
    post = models.CharField(max_length=1000, verbose_name ="게시글")
    emotion = models.CharField( max_length=30, verbose_name="감정정보", null=True)
    pub_date = models.DateTimeField()

    def __str__(self):
        return '%s %s'%(self.insta, self.emotion)

class MusicBox(models.Model):
    emoti = models.CharField(max_length=30, verbose_name="emotion name",)
    url = models.URLField('URL', unique=True)

    def __str__(self):
        return self.emoti