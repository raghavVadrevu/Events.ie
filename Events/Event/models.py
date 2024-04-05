from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    organizer = models.ForeignKey(User, related_name='organized_events', on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='participating_events', blank=True)
    date_from = models.DateField(verbose_name='Start Date', default=timezone.now)
    date_to = models.DateField(verbose_name='End Date', default=timezone.now)

    def __str__(self):
        return self.title
