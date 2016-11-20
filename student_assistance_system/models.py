from __future__ import unicode_literals

import calendar
from collections import defaultdict
import pickle

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
    course_number = models.CharField(max_length=4)
    department = models.ForeignKey(Department)
    credit_hours = models.IntegerField()
    prereqs = models.ManyToManyField('self', symmetrical=False)
    also_offered_as = models.ManyToManyField('self')

    def __unicode__(self):
        return self.name


class Requirement(models.Model):
    name = models.CharField(max_length=50)
    required_hours = models.IntegerField(default=None, blank=True, null=True)
    required_classes = models.IntegerField(default=None, blank=True, null=True)
    query = models.TextField()

    def get_course_set(self):
        course_set = Course.objects.all()
        course_set.query = pickle.loads(self.query)
        return course_set

    def get_course_statuses(self, user, schedule):
        """
        Gets the statuses for the set of courses that can fulfill this requirement.
        Possible status values: 'U' is unfulfilled, 'F' is fulfilled, and 'S' is fulfilled by the schedule
        :param user:
        :param schedule:
        :return: A dict mapping courses to statuses
        """
        course_set = self.get_course_set()
        course_statuses = dict.fromkeys(course_set, 'U')
        for cc in user.profile.completedcourse_set.filter(course__in=course_set):
            course_statuses[cc.course] = 'F'
        for section in schedule.sections.filter(course__in=course_set):
            course_statuses[section.course] = 'S'
        return course_statuses

    def fulfillment_status(self, course_statuses):
        """
        Gets the overall status for the requirement given the fulfillment statuses of its course set
        Possible status values: 'U' is unfulfilled, 'F' is fulfilled, and 'S' is fulfilled by the schedule
        :param course_statuses:
        :return: The overall status for the requirement
        """
        completed = [course for course, status in course_statuses.items() if status == 'F']
        scheduled = [course for course, status in course_statuses.items() if status == 'S']
        if self.required_hours is not None:
            hours = sum([course.credit_hours for course in completed], 0)
            if hours >= self.required_hours:
                return 'F'
            hours += sum([course.credit_hours for course in scheduled], 0)
            return 'S' if hours >= self.required_hours else 'U'
        else:
            count = len(completed)
            if count >= self.required_classes:
                return 'F'
            count += len(scheduled)
            return 'S' if count >= self.required_classes else 'U'

    def __unicode__(self):
        return self.name


def create_requirement(requirement_name, required_hours, required_classes, queryset):
    if (required_hours is None) ^ (required_classes is None):
        query = pickle.dumps(queryset.query)
        return Requirement.objects.create(name=requirement_name,
                                          required_hours=required_hours,
                                          required_classes=required_classes,
                                          query=query)
    else:
        raise ValueError('One of required_hours and required_classes must be None and the other must have a value')


class RequirementSet(models.Model):
    name = models.CharField(max_length=50)
    department = models.ForeignKey(Department)
    type = models.IntegerField()  # 0 = major, 1 = minor, 2 = concentration
    effective_date = models.DateField()
    requirements = models.ManyToManyField(Requirement)

    def __unicode__(self):
        return self.name

    def type_name(self):
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

    def day_abbr(self):
        return ['M', 'T', 'W', 'Th', 'F', 'Sa', 'Su'][self.day]

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

    def condensed_meeting_times(self):
        times = defaultdict(list)
        for time in self.meeting_times.all():
            times[(time.start_time, time.end_time)].append(time.day_abbr())
        return [''.join(days) + ' ' + st.strftime('%-I:%M%p') + ' - ' + end.strftime('%-I:%M%p') for (st, end), days in times.iteritems()]




class Schedule(models.Model):
    name = models.CharField(max_length=50)
    sections = models.ManyToManyField(Section)
    user = models.ForeignKey(Profile)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def delete_section(self, section):
        if section is None:
            raise ValueError('No Section Selected')
        self.sections.remove(section)
        self.save()


class CompletedCourse(models.Model):
    user = models.ForeignKey(Profile)
    course = models.ForeignKey(Course)
    grade = models.CharField(max_length=1)


class UserMajor(models.Model):
    name = models.ForeignKey(Profile)
    major = models.ForeignKey(RequirementSet)
    concentration = models.ForeignKey(RequirementSet, related_name='+')
