from django import template
from student_assistance_system.models import Schedule

register = template.Library()


@register.inclusion_tag('student_assistance_system/schedule_view.html')
def schedule_view(schedule):
    """
    :type schedule: Schedule
    """
    assert isinstance(schedule, Schedule)
    return dict(schedule=schedule)
