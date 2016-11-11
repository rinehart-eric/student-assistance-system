from __future__ import unicode_literals

import calendar

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver


class Department(models.Model):
    full_name = models.CharField(max_length=50)
    abbr_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.abbr_name


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=5000)
    course_number = models.CharField(max_length=3)
    department = models.ForeignKey(Department)
    credit_hours = models.IntegerField()
    prereqs = models.ManyToManyField('self', symmetrical=False)
    also_offered_as = models.ManyToManyField('self')

    def __unicode__(self):
        return self.name


class Requirement(models.Model):
    name = models.CharField(max_length=50)
    required_hours = models.IntegerField()
    required_classes = models.IntegerField()
    query = models.CharField(max_length=500)


class RequirementSet(models.Model):
    name = models.CharField(max_length=50)
    department = models.ForeignKey(Department)
    type = models.IntegerField() # 0 = major, 1 = minor, 2 = concentration
    effective_date = models.DateField()
    requirements = models.ManyToManyField(Requirement)

    def __unicode__(self):
        return self.name

    def requirementset_type(self):
        return {
            0: 'Major',
            1: 'Minor',
            2: 'Concentration',
        }[self.type]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    minors = models.ManyToManyField(RequirementSet)
    year = models.CharField(max_length=50)


# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class MeetingTime(models.Model):
    day = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __unicode__(self):
        return ' '.join((calendar.day_name[self.day],
                         self.start_time.strftime('%H:%M'),
                         '-',
                         self.end_time.strftime('%H:%M')))


class Section(models.Model):
    course = models.ForeignKey(Course)
    capacity = models.IntegerField()
    enrolled = models.IntegerField()
    meeting_times = models.ManyToManyField(MeetingTime)
    professor = models.CharField(max_length=30)
    location = models.CharField(max_length=30)

class Schedule(models.Model):
    name = models.CharField(max_length=50)
    sections = models.ManyToManyField(Section)
    user = models.ForeignKey(Profile)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class CompletedCourse(models.Model):
    user = models.ForeignKey(Profile)
    course = models.ForeignKey(Course)
    grade = models.CharField(max_length=1)


class UserMajor(models.Model):
    name = models.ForeignKey(Profile)
    major = models.ForeignKey(RequirementSet)
    concentration = models.ForeignKey(RequirementSet, related_name='+')
