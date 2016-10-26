from __future__ import unicode_literals

from django.db import models


class Department(models.Model):
    full_name = models.CharField(max_length=50)
    abbr_name = models.CharField(max_length=50)


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=5000)
    course_number = models.CharField(max_length=3)
    department = models.ForeignKey(Department)
    credit_hours = models.IntegerField()
    prereqs = models.ManyToManyField('self', symmetrical=False)
    also_offered_as = models.ManyToManyField('self')


class Requirement(models.Model):
    name = models.CharField(max_length=50)
    required_hours = models.IntegerField()
    required_classes = models.IntegerField()
    query = models.CharField(max_length=500)


class RequirementSet(models.Model):
    name = models.CharField(max_length=50)
    department = models.ForeignKey(Department)
    type = models.IntegerField()
    effective_date = models.DateField()
    requirements = models.ManyToManyField(Requirement)


class User(models.Model):
    name = models.CharField(max_length=50)
    minors = models.ManyToManyField(RequirementSet)


class Section(models.Model):
    course = models.ForeignKey(Course)
    capacity = models.IntegerField()
    enrolled = models.IntegerField()
    professor = models.CharField(max_length=30)
    location = models.CharField(max_length=30)


class MeetingTime(models.Model):
    section = models.ForeignKey(Section)
    day = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()


class Schedule(models.Model):
    name = models.CharField(max_length=50)
    sections = models.ManyToManyField(Section)
    user = models.ForeignKey(User)


class CompletedCourse(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    grade = models.CharField(max_length=1)


class UserMajor(models.Model):
    name = models.ForeignKey(User)
    major = models.ForeignKey(RequirementSet)
    concentration = models.ForeignKey(RequirementSet, related_name='+')









