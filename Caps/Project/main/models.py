from django.db import models
from django.utils import timezone

# Create your models here.

class Guest(models.Model):
    insta=models.CharField(max_length=30)

    def __str__(self):
        return self.insta


class Calender(models.Model):
    insta_id = models.ForeignKey("Guest", on_delete=models.CASCADE,db_column="insta_id")
    emotion = models.CharField(help_text="today emotion", max_length=30)
    pub_date = models.DateTimeField(default=timezone.now,null=True)

    class Meta :
        ordering=('-pub_date',)

  