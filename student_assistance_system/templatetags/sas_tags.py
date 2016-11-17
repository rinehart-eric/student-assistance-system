from django import template

register = template.Library()


@register.inclusion_tag('student_assistance_system/fragments/schedule_view.html')
def schedule_view(schedule):
    return dict(schedule=schedule)


@register.inclusion_tag('student_assistance_system/fragments/requirements_view.html', takes_context=True)
def requirements_view(context, req_sets):
    return dict(user=context['user'], req_sets=req_sets, schedule=context['schedule'])


@register.simple_tag
def get_course_statuses(requirement, user, schedule):
    return requirement.get_course_statuses(user, schedule)


@register.simple_tag
def fulfillment_status(requirement, course_statuses):
    return requirement.fulfillment_status(course_statuses)
