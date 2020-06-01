from django.contrib.auth.models import User
from django.db import models


# Create your models here.
import datetime
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(verbose_name="first name", max_length=50)
    lastname = models.CharField(verbose_name="last name", max_length=50)
    phonenumber = models.CharField(verbose_name="phone number", max_length=10)
    email = models.CharField(verbose_name="email", max_length=100)

class Comments(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.CharField(max_length=2000)
    comment_date = models.DateTimeField('commented date')

    def __str__(self):
        return self.comment + ' ' + self.comment_date + ' : '+self.user

class Projects(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)


class Tasks(models.Model):
    projectID = models.ForeignKey(Projects, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)


class Timers(models.Model):
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    taskID = models.ForeignKey(Tasks, on_delete=models.CASCADE)


class TaskNotes(models.Model):
    note = models.TextField(max_length=250)
    taskID = models.ForeignKey(Tasks, on_delete=models.CASCADE)


class ProjectNotes(models.Model):
    note = models.TextField(max_length=250)
    projectID = models.ForeignKey(Projects, on_delete=models.CASCADE)

