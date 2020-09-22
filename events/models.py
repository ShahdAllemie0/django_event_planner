from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title=models.CharField(max_length=120)
    description=models.TextField()
    date=models.DateField()
    time=models.TimeField()
    location=models.CharField(max_length=100)
    seats=models.PositiveIntegerField()
    organizer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='events')

    def __str__(self):
        return self.title


class EventGuest(models.Model):
    guest=models.ForeignKey(User,on_delete=models.CASCADE,related_name='guest')
    seats=models.PositiveIntegerField()
    event=models.ForeignKey(Event,on_delete=models.CASCADE,related_name='gustevent')


    def __str__(self):
        return "%s-%s"%(self.guest,self.event)

class UserProfile(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE)
